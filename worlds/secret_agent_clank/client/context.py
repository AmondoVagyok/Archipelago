import asyncio
from typing import Any

from NetUtils import ClientStatus

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import UT_VERSION, TrackerGameContext as CommonContext
    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext
from CommonClient import logger

dynamicpine_loaded = False
try:
    from worlds.dynamicpine import DYNAMIC_PINE_VERSION, get_pending_auth, get_pine_port, launched_via_hub
    dynamicpine_loaded = True
except ImportError:
    DYNAMIC_PINE_VERSION = None

from ..constants.weapons import GADGET_DISPLAY_TO_INTERNAL, RATCHET_WEAPON_DISPLAY_TO_INTERNAL
from ..core.core import Core
from ..items import GADGET_ITEM_TABLE, TRAP_ITEM_TABLE, WEAPON_ITEM_TABLE

# WEAPON_ITEM_TABLE's keys are AP-facing "Unlock: {Character} {internal name}"
# display names (constants/weapons.py's SACRatchetWeapons / constants/
# clank_gadgets.py's SACClankGadgets) -- Core's
# apply_inventory()/case.ratchet_items expect raw WEAPON_ORDER internal names
# instead (e.g. "shockrocket"), so this is the display -> internal translation
# for _apply_received_items()'s `ratchet` dict below.
_WEAPON_TABLE_DISPLAY_TO_INTERNAL: dict[str, str] = {
    **RATCHET_WEAPON_DISPLAY_TO_INTERNAL,
    **GADGET_DISPLAY_TO_INTERNAL,
}
from ..locations import ALL_LOCATIONS
from ..pypine import Pine
from .command_processor import SACCommandProcessor
from .constants import GAME_NAME
from .deathlink import DeathLinkMixin
from .pine_mixin import PineMixin


class SACContext(PineMixin, DeathLinkMixin, CommonContext):
    game = GAME_NAME
    command_processor = SACCommandProcessor
    items_handling = 0b111
    current_planet: str = "Galaxy"
    # This is a real game client (syncs live PCSX2 memory), not the passive
    # "Tracker" connection UT's own headless client uses -- dropping this
    # tag keeps the server from treating this connection as tracker-only
    # when worlds.tracker's TrackerGameContext is the resolved base above.
    tags = CommonContext.tags - {"Tracker"}

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)

        self.pine = Pine()
        self.pine_connected = False
        self._pine_lock = asyncio.Lock()
        self.slot_data: dict[str, Any] = {}

        self._location_name_to_id = {name: data.code for name, data in ALL_LOCATIONS.items()}
        self._locally_checked_locations: set[int] = set()
        # Names already warned about via _append_location_by_name (pine_mixin.py)
        # -- native detectors retry a rejected name every tick (see
        # core/case_events.py's confirm() docstring for why that retry
        # matters), but a name genuinely absent from this seed (e.g. a
        # disabled character's case) will never stop being rejected, so
        # only the first rejection is logged to avoid spamming the console.
        self._warned_missing_locations: set[str] = set()

        self._death_link_enabled = False
        self._last_death_link = 0.0
        self._processed_trap_count = 0
        self._notification_count = None
        self._notification_slot = None

        self._wiring = Core(self.pine, log=logger.info)
        from ..rules.vendor_access import VENDOR_REQUIREMENTS
        from rule_builder.rules import False_
        self._wiring.native_runtime.configure_vendors(
            name for name, rule in VENDOR_REQUIREMENTS.items() if not isinstance(rule, False_))

    async def _apply_received_items(self) -> None:
        """Rebuild the per-character AP-ownership snapshot from
        items_received and hand it to Core.apply_inventory(), which writes
        it into game memory (gated on the current case being ready)."""
        if self.slot is None or not self.pine_connected:
            return
        received_names = [
            self.item_names[self.game].get(network_item.item, "")
            for network_item in self.items_received
        ]
        ratchet = {
            _WEAPON_TABLE_DISPLAY_TO_INTERNAL[name]: name in received_names
            for name in WEAPON_ITEM_TABLE
        }
        clank   = {name: name in received_names for name in GADGET_ITEM_TABLE}
        async with self._pine_lock:
            try:
                self._wiring.apply_inventory(ratchet=ratchet, clank=clank, received_names=received_names)
                if self._notification_count is not None:
                    for index in range(self._notification_count, len(received_names)):
                        item = self.items_received[index]
                        sender = self.player_names.get(item.player, f'Player {item.player}')
                        self._wiring.notifications.enqueue(received_names[index], sender, bool(item.flags & 4))
                if self._notification_count is not None or received_names:
                    self._notification_count = max(self._notification_count or 0, len(received_names))
            except Exception as exc:
                logger.warning(f"[SAC] PINE call failed while applying items: {exc}. "
                                "If syncing stops working, use /reconnect.")
                self.pine_connected = False
                return
        await self._apply_new_traps(received_names)

    async def _apply_new_traps(self, received_names: list[str]) -> None:
        """Fires activate_trap() once per trap item beyond what's already
        been processed this session -- received_names is index-ordered, so
        slicing from _processed_trap_count only sees genuinely new items."""
        new_traps = [name for name in received_names[self._processed_trap_count:] if name in TRAP_ITEM_TABLE]
        self._processed_trap_count = len(received_names)
        if not new_traps:
            return
        async with self._pine_lock:
            try:
                for name in new_traps:
                    self._wiring.activate_trap(name)
            except Exception as exc:
                logger.warning(f"[SAC] PINE call failed while activating a trap: {exc}. "
                                "If syncing stops working, use /reconnect.")
                self.pine_connected = False

    def _checked_location_names(self) -> set[str]:
        id_to_name = {v: k for k, v in self._location_name_to_id.items()}
        return {
            id_to_name[lid]
            for lid in (self.checked_locations | self._locally_checked_locations)
            if lid in id_to_name
        }

    def _dynamic_pine_auth(self) -> None:
        """Pre-fills auth from whatever slot name the hub's /launch command
        was given, so the player isn't asked to retype it -- and so it
        can't drift from what _dynamic_pine_port() later looks the PCSX2
        instance's port up under. Gated on launched_via_hub() and only
        applied when auth isn't already set some other way."""
        if self.auth or not dynamicpine_loaded:
            return
        if not launched_via_hub():
            return
        pending = get_pending_auth()
        if pending:
            self.auth = pending

    def _dynamic_pine_port(self) -> None:
        """This world uses launcher_options="simple" -- the hub's Launch
        button always starts PCSX2 itself before spawning this client, so
        this only ever resolves the already-assigned port, never launches
        anything. Gated on launched_via_hub() the same way as
        _dynamic_pine_auth() -- a normal (non-hub) launch just uses Pine's
        own default port."""
        if not self.auth or not dynamicpine_loaded:
            return
        if not launched_via_hub():
            return
        port = get_pine_port(GAME_NAME, self.auth)
        if port is not None:
            self.pine.set_slot(port)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        self._dynamic_pine_auth()
        await self.get_username()
        await self.send_connect(game=self.game)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        super().on_package(cmd, args)

        if cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
            return

        if cmd == "Connected":
            identity = (self.seed_name, self.team, self.slot)
            if identity != self._notification_slot:
                self._notification_slot = identity
                self._notification_count = None
                self._wiring.notifications.queue.clear()
            self.slot_data = args.get("slot_data", {})
            self._wiring.native_runtime.starting_case.configure(self.slot_data)
            self._wiring.bolt_rewards.configure(
                self.seed_name, self.team, self.slot,
                starting_bolts=int(self.slot_data.get('starting_bolts', 0)))
            self._wiring.progression.configure(self.slot_data)
            self._wiring.weapon_mods.configure(self.slot_data)
            self._wiring.wrench.enabled = bool(self.slot_data.get("progressive_wrench", False))
            self._wiring.character_unlocks = int(self.slot_data.get("infobots", 1)) == 3
            self._wiring.goal = int(self.slot_data.get('goal', 0))
            self._wiring._goal_sent = False  # Resend after reconnect if the earlier status was lost.
            self._death_link_enabled = bool(self.slot_data.get("death_link", False))
            if self._death_link_enabled:
                self.tags |= {"DeathLink"}
                asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": list(self.tags)}]))

            self._wiring.wire(
                send_location      = self._append_location_by_name,
                send_deathlink     = self._send_death_link_from_sync,
                death_amnesty      = lambda: int(self.slot_data.get("death_amnesty", 1)),
                death_link_enabled = lambda: self._death_link_enabled,
                on_case_ready      = lambda: None,
                on_goal            = self._send_goal,
                # slot_data's "all_missions" is options.py's Missions
                # value (0 = level_completion, 1 = all -- see world.py's
                # fill_slot_data()).
                missions_all       = lambda: self.slot_data.get("all_missions", 0) == 1,
            )
            checked = self._checked_location_names()
            asyncio.create_task(self._pine_guarded(lambda: self._wiring.sync_from_ap(checked)))
            asyncio.create_task(self._apply_received_items())

            if not self.pine_connected:
                self._dynamic_pine_port()
                asyncio.create_task(self._attempt_pine_connect(), name="PCSX2 PINE connect")
            return

        if cmd == "ReceivedItems" and self._notification_count is None:
            # Initial sync is historical inventory, not a burst of new receipts.
            self._notification_count = len(self.items_received)

        if cmd in ("ReceivedItems", "RoomUpdate"):
            checked = self._checked_location_names()
            asyncio.create_task(self._pine_guarded(lambda: self._wiring.sync_from_ap(checked)))
            asyncio.create_task(self._apply_received_items())
            return

        if cmd == "Bounced" and self._death_link_enabled and "DeathLink" in args.get("tags", []):
            data = args.get("data", {})
            if data.get("source") != self.auth:
                asyncio.create_task(self._receive_death_link(data))

    async def _pine_guarded(self, fn) -> None:
        async with self._pine_lock:
            try:
                fn()
            except Exception as exc:
                logger.warning(f"[SAC] PINE call failed during wiring sync: {exc}. "
                                "If syncing stops working, use /reconnect.")
                self.pine_connected = False

    def _send_goal(self):
        self.finished_game = True
        asyncio.create_task(self.send_msgs([{'cmd': 'StatusUpdate', 'status': ClientStatus.CLIENT_GOAL}]))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Secret Agent Clank Client"
        if dynamicpine_loaded:
            ui.base_title += f" | Dynamic Pine v{DYNAMIC_PINE_VERSION}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"
        ui.base_title += " | Archipelago"
        return ui

import asyncio
from typing import Any

from CommonClient import logger
from NetUtils import ClientStatus
from rule_builder.rules import False_
from Utils import async_start

from ..constants.weapons import EQUIPMENT_DISPLAY_TO_INTERNAL
from ..core.core import Core
from ..items import GADGET_ITEM_TABLE, TRAP_ITEM_TABLE, WEAPON_ITEM_TABLE
from ..locations import LOCATION_NAME_TO_ID
from ..pypine import Pine
from ..rules.vendor_access import VENDOR_REQUIREMENTS
from .command_processor import SACCommandProcessor
from .constants import GAME_NAME
from .deathlink import DeathLinkMixin
from .item_names import canonical_item_name
from .pine_mixin import PineMixin
from .vendor_scouts import VendorScouts

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import UT_VERSION
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext
    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext

dynamicpine_loaded = False
try:
    from worlds.dynamicpine import DYNAMIC_PINE_VERSION, get_pending_auth, get_pine_port, launched_via_hub
    dynamicpine_loaded = True
except ImportError:
    DYNAMIC_PINE_VERSION = None


class SACContext(PineMixin, DeathLinkMixin, CommonContext):
    game = GAME_NAME
    command_processor = SACCommandProcessor
    items_handling = 0b111
    current_planet: str = "Galaxy"
    # A real game client, so drop the "Tracker" tag UT's context would otherwise add.
    tags = CommonContext.tags - {"Tracker"}

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)

        self.pine = Pine()
        self.pine_connected = False
        self._pine_lock = asyncio.Lock()
        self.slot_data: dict[str, Any] = {}

        self._location_name_to_id = dict(LOCATION_NAME_TO_ID)
        self.vendor_scouts = VendorScouts(self._location_name_to_id)
        # Location ids already scouted this connection (see _maybe_scout_vendor()).
        self._scouted_location_ids: set[int] = set()
        self._locally_checked_locations: set[int] = set()
        # Rejected location names already logged; detectors retry them every tick.
        self._warned_missing_locations: set[str] = set()

        self._death_link_enabled = False
        self._last_death_link = 0.0
        # None until _load_trap_state() has read the count from the server.
        self._processed_trap_count: int | None = None
        self._notification_count = None
        self._notification_slot = None
        self._stealth_identity = None
        self._stealth_load_task = None

        self._wiring = Core(self.pine, log=logger.info)
        self._wiring.vendor_rewards.scouts = self.vendor_scouts
        self._wiring.native_runtime.configure_vendors(
            name for name, rule in VENDOR_REQUIREMENTS.items() if not isinstance(rule, False_))

    async def _load_stealth_state(self, key, state):
        self.stored_data.pop(key, None)
        await self.send_msgs([{"cmd": "Set", "key": key, "want_reply": True,
                               "operations": [{"operation": "default", "value": 0}]}])
        while key not in self.stored_data:
            await asyncio.sleep(0.1)
        state.load(self.stored_data[key])
        # Retry any progress whose write was interrupted by a disconnect.
        state.on_count(state.count)

    def _configure_stealth(self, identity):
        if self._stealth_load_task is not None:
            self._stealth_load_task.cancel()
        state = self._wiring.stealth
        state.configure(int(self.slot_data.get("stealth_takedown_checks", 0)),
                        reset=identity != self._stealth_identity)
        self._stealth_identity = identity
        key = f"secret_agent_clank_stealth_{self.team}_{self.slot}"
        def save(count):
            async_start(self.send_msgs([
                {"cmd": "Set", "key": key,
                 "operations": [{"operation": "max", "value": count}]}]))
        state.on_count = save
        if state.mode:
            self._stealth_load_task = asyncio.create_task(self._load_stealth_state(key, state))

    def _bolt_storage_keys(self) -> tuple[str, str]:
        """Server data-storage keys for this slot's delivered and pending bolt rewards."""
        return (f"secret_agent_clank_delivered_bolts_{self.team}_{self.slot}",
                f"secret_agent_clank_pending_bolts_{self.team}_{self.slot}")

    async def _load_bolt_state(self) -> None:
        """Load bolt-reward state from the server, then enable delivery so rewards are never granted twice."""
        delivered_key, pending_key = self._bolt_storage_keys()
        # Drop cached values from an earlier connection so the wait below sees fresh ones.
        self.stored_data.pop(delivered_key, None)
        self.stored_data.pop(pending_key, None)
        await self.send_msgs([
            {"cmd": "Set", "key": delivered_key, "want_reply": True, "operations": [
                {"operation": "default", "value": {"count": 0, "starting_delivered": False}}]},
            {"cmd": "Set", "key": pending_key, "want_reply": True,
             "operations": [{"operation": "default", "value": None}]},
        ])
        while delivered_key not in self.stored_data or pending_key not in self.stored_data:
            await asyncio.sleep(0.1)
        delivered = self.stored_data[delivered_key]
        if not isinstance(delivered, dict):
            # Older clients stored a bare count here.
            delivered = {"count": int(delivered), "starting_delivered": False}
        self._wiring.bolt_rewards.configure(
            starting_bolts=int(self.slot_data.get("starting_bolts", 0)),
            delivered=delivered["count"],
            starting_delivered=delivered["starting_delivered"],
            pending=self.stored_data[pending_key],
        )

    def _save_bolt_state(self, delivered: dict, pending: "dict | None") -> None:
        """Persist bolt-reward state to server data storage."""
        delivered_key, pending_key = self._bolt_storage_keys()
        async_start(self.send_msgs([
            {"cmd": "Set", "key": delivered_key, "operations": [{"operation": "replace", "value": delivered}]},
            {"cmd": "Set", "key": pending_key, "operations": [{"operation": "replace", "value": pending}]},
        ]))

    def _trap_storage_key(self) -> str:
        """Server data-storage key for how many received items have been processed for traps."""
        return f"secret_agent_clank_processed_traps_{self.team}_{self.slot}"

    async def _load_trap_state(self) -> None:
        """Load the processed-trap count, so reconnecting doesn't replay every trap ever received."""
        key = self._trap_storage_key()
        self.stored_data.pop(key, None)
        await self.send_msgs([
            {"cmd": "Set", "key": key, "want_reply": True, "operations": [{"operation": "default", "value": 0}]},
        ])
        while key not in self.stored_data:
            await asyncio.sleep(0.1)
        self._processed_trap_count = self.stored_data[key]
        # Traps are only applied on item events, so apply any that arrived while loading.
        async_start(self._apply_received_items())

    def _save_trap_state(self, count: int) -> None:
        async_start(self.send_msgs(
            [{"cmd": "Set", "key": self._trap_storage_key(), "operations": [{"operation": "replace", "value": count}]}]
        ))

    async def _apply_received_items(self) -> None:
        """Pass every received item to Core, queue receipt notifications, then fire new traps."""
        if self.slot is None or not self.pine_connected:
            return
        received_names = [
            canonical_item_name(self.item_names[self.game].get(network_item.item, ""))
            for network_item in self.items_received
        ]
        ratchet = {
            EQUIPMENT_DISPLAY_TO_INTERNAL[name]: name in received_names
            for name in WEAPON_ITEM_TABLE
        }
        clank   = {name: name in received_names for name in GADGET_ITEM_TABLE}
        async with self._pine_lock:
            try:
                self._wiring.apply_inventory(ratchet=ratchet, clank=clank, received_names=received_names)
                if self._notification_count is not None:
                    for index in range(self._notification_count, len(received_names)):
                        item = self.items_received[index]
                        sender = self.player_names.get(item.player, f"Player {item.player}")
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
        """Activate each trap received since the last processed index, stopping at one that can't fire yet."""
        if self._processed_trap_count is None:
            return
        async with self._pine_lock:
            try:
                for index in range(self._processed_trap_count, len(received_names)):
                    name = received_names[index]
                    if name in TRAP_ITEM_TABLE and not self._wiring.activate_trap(name):
                        break
                    self._processed_trap_count = index + 1
                    self._save_trap_state(self._processed_trap_count)
            except Exception as exc:
                logger.warning(f"[SAC] Trap activation deferred: {exc}")

    def _checked_location_names(self) -> set[str]:
        id_to_name = {v: k for k, v in self._location_name_to_id.items()}
        return {
            id_to_name[lid]
            for lid in (self.checked_locations | self._locally_checked_locations)
            if lid in id_to_name
        }

    def _maybe_scout_vendor(self) -> None:
        """Scout the seed's vendor catalog once the shared shop is opened."""
        if self.slot is None or not self._wiring.vendor.active:
            return
        server_locations = getattr(self, "server_locations", None)
        if server_locations is None:
            return
        request = self.vendor_scouts.request(
            server_locations, hint=bool(self.slot_data.get("send_scouted_locations", True)),
            owned_cases=self._wiring.owned_cases,
        )
        new_ids = [lid for lid in request["locations"] if lid not in self._scouted_location_ids]
        if not new_ids:
            return
        self._scouted_location_ids.update(new_ids)
        async_start(self.send_msgs([{**request, "locations": new_ids}]))

    def _dynamic_pine_auth(self) -> None:
        """Use the slot name the Dynamic Pine hub launched us with."""
        if self.auth or not dynamicpine_loaded:
            return
        if not launched_via_hub():
            return
        pending = get_pending_auth()
        if pending:
            self.auth = pending

    def _dynamic_pine_port(self) -> None:
        """Connect to the PCSX2 instance the Dynamic Pine hub started for this slot."""
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

    async def connection_closed(self) -> None:
        if self._stealth_load_task is not None:
            self._stealth_load_task.cancel()
        self._wiring.native_runtime.ap_connected = False
        await super().connection_closed()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        super().on_package(cmd, args)

        if cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
            return

        if cmd == "Connected":
            self._wiring.native_runtime.ap_connected = True
            identity = (self.seed_name, self.team, self.slot)
            if identity != self._notification_slot:
                self._notification_slot = identity
                self._notification_count = None
                self._wiring.notifications.queue.clear()
            self.slot_data = args.get("slot_data", {})
            self._configure_stealth(identity)
            self.vendor_scouts.rewards.clear()
            self._scouted_location_ids.clear()
            self._wiring.native_runtime.starting_case.configure(self.slot_data)
            async_start(self._load_bolt_state())
            async_start(self._load_trap_state())
            self._wiring.progression.configure(self.slot_data)
            self._wiring.skins.configure(self.slot_data)
            self._wiring.weapon_mods.configure(self.slot_data)
            self._wiring.wrench.enabled = bool(self.slot_data.get("progressive_wrench", False))
            self._wiring.progressive_planets = self.slot_data.get("progressive_planets")
            self._wiring.character_unlocks = int(self.slot_data.get("infobots", 1)) == 3
            self._wiring.traps.durations.update(self.slot_data.get("trap_duration", {}))
            self._wiring.goal = int(self.slot_data.get("goal", 0))
            self._wiring._goal_sent = False  # Resend after reconnect if the earlier status was lost.
            self._death_link_enabled = bool(self.slot_data.get("death_link", False))
            if self._death_link_enabled:
                self.tags |= {"DeathLink"}
                async_start(self.send_msgs([{"cmd": "ConnectUpdate", "tags": list(self.tags)}]))

            self._wiring.wire(
                send_location      = self._append_location_by_name,
                send_deathlink     = self._send_death_link_from_sync,
                death_amnesty      = lambda: int(self.slot_data.get("death_amnesty", 1)),
                death_link_enabled = lambda: self._death_link_enabled,
                on_goal            = self._send_goal,
                # Missions option: 0 = level_completion, 1 = all.
                missions_all       = lambda: self.slot_data.get("all_missions", 0) == 1,
                on_bolt_state_changed = self._save_bolt_state,
            )
            self._wiring.native_runtime.vendor_locations = {
                name for name, location_id in self._location_name_to_id.items()
                if location_id in self.server_locations
            }
            self._resync_from_ap()

            if not self.pine_connected:
                self._dynamic_pine_port()
                async_start(self._attempt_pine_connect(), name="PCSX2 PINE connect")
            return

        if cmd in ("LocationInfo", "DataPackage", "RoomUpdate"):
            self.vendor_scouts.update(
                self.locations_info.values(), self.item_names.lookup_in_slot,
                lambda slot: self.player_names.get(slot, f"Player {slot}"))

        if cmd == "ReceivedItems" and self._notification_count is None:
            # Initial sync is historical inventory, not a burst of new receipts.
            self._notification_count = len(self.items_received)

        if cmd in ("ReceivedItems", "RoomUpdate"):
            self._resync_from_ap()
            return

        if cmd == "Bounced" and self._death_link_enabled and "DeathLink" in args.get("tags", []):
            data = args.get("data", {})
            if data.get("source") != self.auth:
                async_start(self._receive_death_link(data))

    def _resync_from_ap(self) -> None:
        """Push AP's checked locations into the game, then re-apply received items."""
        checked = self._checked_location_names()
        async_start(self._pine_guarded(lambda: self._wiring.sync_from_ap(checked)))
        async_start(self._apply_received_items())

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
        async_start(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Secret Agent Clank Client"
        if dynamicpine_loaded:
            ui.base_title += f" | Dynamic Pine v{DYNAMIC_PINE_VERSION}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"
        ui.base_title += " | Archipelago"
        return ui

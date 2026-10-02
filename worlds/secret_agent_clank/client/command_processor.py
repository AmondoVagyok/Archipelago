from typing import TYPE_CHECKING

from CommonClient import logger
from Utils import async_start

try:
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as ClientCommandProcessor
except ImportError:
    from CommonClient import ClientCommandProcessor

from ..constants.planets import ALL_CASES, Case

if TYPE_CHECKING:
    from .context import SACContext


class SACCommandProcessor(ClientCommandProcessor):
    ctx: "SACContext"

    def _match_case(self, case: str) -> "Case | None":
        """Case-insensitive substring match against every known case name."""
        matches = [c for c in ALL_CASES if case.lower() in c.name.lower()]
        if not matches:
            logger.warning(f"[SAC] No case matches {case!r}.")
            return None
        if len(matches) > 1:
            logger.warning(f"[SAC] {case!r} matches multiple cases: " + ", ".join(c.name for c in matches))
            return None
        return matches[0]

    def _resolve_case_id(self, case: str, command: str) -> "int | None":
        """The named case's id, or the current one when no name is given; warns and returns None if unknown."""
        if case:
            match = self._match_case(case)
            return match.case_id if match is not None else None
        if self.ctx._wiring.case.case_id is None:
            logger.warning(f"[SAC] No current case known -- pass a case name to anchor off, e.g. /{command} museum.")
        return self.ctx._wiring.case.case_id

    def _cmd_reconnect(self) -> bool:
        """Reconnect to PCSX2 and re-apply received Archipelago items."""
        async_start(self.ctx.reconnect_pine())
        return True

    def _cmd_native_locations(self, mode: str = "on") -> bool:
        """Native interception is mandatory; /native_locations off is rejected."""
        if mode.lower() not in ("on", "off"):
            logger.warning("[SAC] Usage: /native_locations on|off")
            return False

        async def change_mode():
            async with self.ctx._pine_lock:
                try:
                    self.ctx._wiring.set_native_locations(mode.lower() == "on")
                except Exception as exc:
                    logger.warning(f"[SAC] Native location mode: {exc}")
        async_start(change_mode())
        return True

    def _cmd_sac_info(self) -> bool:
        """Print the slot options and the state of every tracker (read-only)."""
        ctx = self.ctx
        options = "\n".join(f"{key}: {value}" for key, value in ctx.slot_data.items())
        logger.info(f"[SAC] Options:\n{options}")

        w = ctx._wiring
        states = (
            w.case, w.case.ratchet, w.case.clank, w.case.qwark, w.vendor, w.missions,
            w.titanium_bolts, w.skill_points, w.cutscenes,
            w.gadgetbot_challenges, w.special_challenges, w.ratchet_challenges,
            w.quick_select, w.case_struct,
        )
        logger.info("[SAC] States: " + " ".join(repr(state) for state in states))

        owned_ratchet = {name: v for name, v in w._ap_owned.get("ratchet", {}).items() if v}
        owned_equipment = {name: v for name, v in w._owned_equipment().items() if v}
        hooks = w.native_runtime.hooks
        logger.info(
            f"[SAC] inventory_initialized={w._inventory_initialized} "
            f"bound_weapons={len(w.case.ratchet_items.weapons)} "
            f"ap_owned_ratchet_true={sorted(owned_ratchet)} "
            f"owned_equipment_true={sorted(owned_equipment)}"
        )
        logger.info(
            f"[SAC] native: awaiting_start={w.native_runtime.awaiting_start} "
            f"generation={w.native_runtime.generation} "
            f"hooks.installed={hooks.installed} hooks.is_current={hooks.is_current()} "
            f"entitlement_table={hooks.entitlement_table!r}"
        )
        return True

    def _cmd_mission_table(self) -> bool:
        """Print each chapter-table slot's task count and whether it matches the cases found in it."""
        w = self.ctx._wiring
        rows = w.missions.dump_chapter_table()
        if not rows:
            logger.warning("[SAC] Couldn't resolve the chapter table right now -- game still loading?")
            return True
        for row in rows:
            if row.assumed_case is None:
                logger.info(f"[SAC] slot {row.slot}: {row.task_count} task(s) -- no case currently assumed here")
                continue
            label = "OK" if row.matches else "MISMATCH"
            logger.info(
                f"[SAC] slot {row.slot}: {row.task_count} task(s) -- "
                f"assumed {row.assumed_case!r} expects {row.expected_count} -- {label}"
            )
        return True

    def _cmd_case_states(self, case: str = "") -> bool:
        """Batch-read and print every case's current locked/unlocked byte."""
        w = self.ctx._wiring
        current_case_id = self._resolve_case_id(case, "case_states")
        if current_case_id is None:
            return True

        states = w.case_unlocks.read_all(current_case_id)
        if not states:
            logger.warning(
                f"[SAC] Couldn't resolve the unlock table off case id {current_case_id} -- "
                "its anchor isn't confirmed live yet."
            )
            return True

        for c in ALL_CASES:
            state = states.get(c.name)
            label = state.name if state is not None else "UNKNOWN"
            logger.info(f"[SAC] {c.name}: {label}")
        return True

    def _cmd_case_struct(self, case: str = "") -> bool:
        """Print every raw case-unlock table slot (0 = locked, 3 = unlocked) and its case, if identified."""
        w = self.ctx._wiring
        current_case_id = self._resolve_case_id(case, "case_struct")
        if current_case_id is None:
            return True

        slots = w.case_struct.read_all(current_case_id)
        if not slots:
            logger.warning(
                f"[SAC] Couldn't resolve the case-unlock table off case id {current_case_id} -- "
                "its anchor isn't confirmed live yet."
            )
            return True

        for slot, value in slots.items():
            case_name = w.case_struct.slot_case_name(slot) or "UNIDENTIFIED"
            logger.info(f"[SAC] slot {slot}: {value} (0x{value:02X}) -- {case_name}")
        return True

    def _cmd_enable_deathlink(self) -> bool:
        """Enable DeathLink for this session."""
        async_start(self.ctx._set_death_link_enabled(True))
        return True

    def _cmd_disable_deathlink(self) -> bool:
        """Disable DeathLink for this session."""
        async_start(self.ctx._set_death_link_enabled(False))
        return True

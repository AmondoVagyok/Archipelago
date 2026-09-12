import asyncio
from typing import TYPE_CHECKING

from CommonClient import logger

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
        """Case-insensitive substring match against every known case name.
        Logs and returns None on no match / an ambiguous match."""
        matches = [c for c in ALL_CASES if case.lower() in c.name.lower()]
        if not matches:
            logger.warning(f"[SAC] No case matches {case!r}.")
            return None
        if len(matches) > 1:
            logger.warning(f"[SAC] {case!r} matches multiple cases: " + ", ".join(c.name for c in matches))
            return None
        return matches[0]

    def _cmd_reconnect(self) -> bool:
        """Reconnect to PCSX2 and re-apply received Archipelago items."""
        asyncio.create_task(self.ctx.reconnect_pine())
        return True

    def _cmd_native_locations(self, mode: str = 'on') -> bool:
        """Native interception is mandatory; /native_locations off is rejected."""
        if mode.lower() not in ('on', 'off'):
            logger.warning('[SAC] Usage: /native_locations on|off')
            return False

        async def change_mode():
            async with self.ctx._pine_lock:
                try:
                    self.ctx._wiring.set_native_locations(mode.lower() == 'on')
                except Exception as exc:
                    logger.warning(f'[SAC] Native location mode: {exc}')
        asyncio.create_task(change_mode())
        return True

    def _cmd_sac_info(self) -> bool:
        """Print the current slot options, then every active state's repr
        -- read-only diagnostics only (user: "remove all the debug give
        items to player from the command processor and instead just have
        a print for the states"); no command here writes game memory."""
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
        return True

    def _cmd_mission_table(self) -> bool:
        """Dump every resolved chapter-table slot (its live task count)
        next to whichever case CASE_ID_TO_CASE currently assumes lives in
        that slot (slot == case_id, only actually confirmed for Boltaire
        Museum's case_id 1 so far) and whether the task counts match.

        A MISMATCH means that case's CHAPTER_ENTRIES addresses are
        currently being resolved off the wrong slot -- use this the same
        way /force_case was used to pin down real case_id values: find
        the slot whose task count actually matches that case's known
        mission count (see constants/missions.py's CHAPTER_ENTRIES) and
        fix up its case_id in constants/planets.py's ALL_CASES to match."""
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
        """Batch-read and print every case's current locked/unlocked byte.
        Resolved off whichever case is currently loaded by default; pass a
        case name (substring match) to anchor off that case instead --
        useful for testing since automatic case-id detection isn't wired
        up to real memory values yet (see CASE_ID_TO_CASE)."""
        w = self.ctx._wiring

        current_case_id = w.case.case_id
        if case:
            match = self._match_case(case)
            if match is None:
                return True
            current_case_id = match.case_id

        if current_case_id is None:
            logger.warning("[SAC] No current case known -- pass a case name to anchor off, e.g. /case_states museum.")
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
        """Batch-read and print every slot of the case-unlock table's
        exact layout (see core/address_maps/ps2.py's
        CASE_UNLOCK_TABLE_OFFSETS / core/case_struct.py's
        CaseStructInventory) -- dumps each slot's raw value (typically 0 =
        LOCKED or 3 = UNLOCKED) plus its identified case name if
        CASE_UNLOCK_TABLE_SLOT_TO_CASE has one yet, so unidentified slots
        stand out. Resolved off whichever case is currently loaded by
        default; pass a case name (substring match) to anchor off that
        case instead."""
        w = self.ctx._wiring

        current_case_id = w.case.case_id
        if case:
            match = self._match_case(case)
            if match is None:
                return True
            current_case_id = match.case_id

        if current_case_id is None:
            logger.warning("[SAC] No current case known -- pass a case name to anchor off, e.g. /case_struct museum.")
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
        asyncio.create_task(self.ctx._set_death_link_enabled(True))
        return True

    def _cmd_disable_deathlink(self) -> bool:
        """Disable DeathLink for this session."""
        asyncio.create_task(self.ctx._set_death_link_enabled(False))
        return True

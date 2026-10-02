"""Read 32-bit mission states by native case label and mission title ID."""
import struct
from typing import TYPE_CHECKING, NamedTuple

from ...constants.missions import (
    ALL_CHAPTER_ENTRIES,
    CHAPTER_ENTRIES,
    COMPLETE_NAME_TO_CASE,
    DISPLAY_NAME_TO_CHAPTER_ENTRY,
    MISSION_COMPLETE_NAME,
    MissionFlag,
)
from ...constants.planets import CASE_NAME_TO_CASE
from ..case_menu import CASE_LABELS
from ..symbols import RuntimeSymbols

if TYPE_CHECKING:
    from ...constants.planets import Case
    from ...pypine import Pine


# The USA module exports g_MISSION_LEVEL_LIST as a direct 33-slot array.
# Verified in live Museum RAM: base 0x5775A0, slot 1 -> 0x576200/count 3.
# The old resolver read the previous export, then compensated with +0x60.
_CHAPTER_TABLE_OFFSET = 0
_CHAPTER_TABLE_SLOTS = 33
_TASK_ENTRY_SIZE = 0x60        # bytes per task entry within a chapter's task array

# Bookkeeping is keyed by native mission names; AP location names are only used
# in check()'s results and confirm()/sync_from_ap()'s inputs.
_TASK_STATE_OFFSET = 0xC       # state field within a task entry (same field CHAPTER_ENTRIES
                                # addresses point at; 1 byte, MissionFlag-valued)

# Sanity limits for a chapter-table slot, so a stale or mid-transition read is ignored.
_PLAUSIBLE_PTR_RANGE: tuple[int, int] = (0x00100000, 0x02000000)  # PS2 EE main RAM, roughly
_PLAUSIBLE_MAX_COUNT = 10


def find_mission_level_list(pine: "Pine") -> "int | None":
    """g_MISSION_LEVEL_LIST's address in the currently loaded module."""
    symbols = RuntimeSymbols(pine)
    symbols.refresh()
    return symbols.get("g_MISSION_LEVEL_LIST")


def resolve_chapter_table(pine: "Pine", base: int | None = None) -> "dict[int, tuple[int, int]]":
    """Read the chapter table's slots as {slot: (pointer, count)}, keeping only plausible ones."""
    if base is None:
        base = find_mission_level_list(pine)
    if base is None:
        return {}
    table_base = base + _CHAPTER_TABLE_OFFSET
    raw = pine.read_bytes(table_base, _CHAPTER_TABLE_SLOTS * 8)
    slots: dict[int, tuple[int, int]] = {}
    lo, hi = _PLAUSIBLE_PTR_RANGE
    for i in range(_CHAPTER_TABLE_SLOTS):
        ptr, count = struct.unpack_from("<II", raw, i * 8)
        if ptr == 0 and count == 0:
            continue
        if lo <= ptr < hi and 0 < count <= _PLAUSIBLE_MAX_COUNT and ptr + count * _TASK_ENTRY_SIZE <= hi:
            slots[i] = (ptr, count)
    return slots


class ChapterTableRow(NamedTuple):
    """One row of MissionInventory.dump_chapter_table()."""
    slot: int
    task_count: int
    assumed_case: "str | None"
    expected_count: "int | None"
    matches: "bool | None"


class MissionInventory:

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine
        self.table_base: int | None = None
        self.completed: dict[str, bool] = dict.fromkeys((entry.name for _, entry in ALL_CHAPTER_ENTRIES), False)
        self._resolved_cases = None
        self._story_addresses = {}
        self._reported = set()
        self._resolved_title_ids = {}

    def sync_from_ap(self, checked_location_names: set[str]) -> None:
        for case_name, complete_name in MISSION_COMPLETE_NAME.items():
            if complete_name in checked_location_names:
                self._reported.add(f"{case_name} Complete")
        for _, entry in ALL_CHAPTER_ENTRIES:
            if entry.display_name in checked_location_names:
                self._reported.add(entry.name)
                self.completed[entry.name] = True

    def invalidate_resolved_addresses(self) -> None:
        """Forget resolved addresses; call on every case transition."""
        self._resolved_cases = None
        self._story_addresses = {}
        self._resolved_title_ids = {}

    def _resolve_labels(self):
        """Native labels identify cases even when they share one module slot."""
        if self._resolved_cases is not None:
            return
        groups, story = {}, {}
        for pointer, count in resolve_chapter_table(self.pine, self.table_base).values():
            data = self.pine.read_bytes(pointer, count * _TASK_ENTRY_SIZE)
            for index in range(count):
                offset = index * _TASK_ENTRY_SIZE
                kind = struct.unpack_from("<I", data, offset)[0]
                label = struct.unpack_from("<I", data, offset + 0x3C)[0]
                name = CASE_LABELS.get(label)
                if name is None or kind not in (1, 4):
                    continue
                address = pointer + offset + _TASK_STATE_OFFSET
                groups.setdefault(name, []).append(address)
                title = struct.unpack_from("<I", data, offset + 4)[0]
                self._resolved_title_ids.setdefault(name, []).append(title)
                if kind == 1:
                    story.setdefault(name, []).append(address)
        if groups:
            self._resolved_cases, self._story_addresses = groups, story

    def check_all(self, *, all_missions=False):
        """Progress can persist into the next module before the next host poll."""
        self._resolve_labels()
        found = []
        for name in self._resolved_cases or {}:
            case = CASE_NAME_TO_CASE.get(name)
            if case is not None:
                found.extend(self.check(case, all_missions=all_missions))
        return found

    def _resolve_case_addresses(self, case: "Case") -> "list[int] | None":
        """Resolve this case by label and verify its native title IDs."""
        self._resolve_labels()
        addresses = (self._resolved_cases or {}).get(case.name)
        titles = self._resolved_title_ids.get(case.name)
        entries = CHAPTER_ENTRIES.get(case.name, ())
        if titles is not None and titles != [entry.title_id for entry in entries]:
            return None
        return addresses

    def check(self, current_case: "Case | None", *, all_missions: bool = True) -> list[str]:
        """Report individual tasks, or the final story task for case completion."""
        newly: list[str] = []
        if current_case is None:
            return newly
        self._resolve_labels()
        if not all_missions:
            story = self._story_addresses.get(current_case.name, ())
            internal_key = f"{current_case.name} Complete"
            if story and internal_key not in self._reported and self.pine.read_int32(story[-1]) == 3:
                return [MISSION_COMPLETE_NAME[current_case.name]]
            return []
        entries = CHAPTER_ENTRIES.get(current_case.name)
        if not entries:
            return newly
        addresses = self._resolve_case_addresses(current_case)
        if addresses is None or len(addresses) != len(entries):
            return newly
        values = self.pine.batch_read_int32(addresses)
        for entry, value in zip(entries, values):
            now = value == MissionFlag.UNLOCKED_COMPLETED
            flipped = now and entry.name not in self._reported
            self.completed[entry.name] = now or self.completed.get(entry.name, False)
            if not flipped:
                continue
            newly.append(entry.display_name)
        return newly

    def confirm(self, name: str) -> None:
        """Stop reporting `name`; call only once AP has accepted the check."""
        case_name = COMPLETE_NAME_TO_CASE.get(name)
        if case_name is not None:
            self._reported.add(f"{case_name} Complete")
            return
        entry = DISPLAY_NAME_TO_CHAPTER_ENTRY.get(name)
        if entry is not None:
            self._reported.add(entry.name)

    def enforce_owned_first_missions(self, owned_cases: "set[str]") -> int:
        """Set each owned case's first mission back to UNLOCKED if it is disabled; returns the write count."""
        first_addresses: list[int] = []
        for case_name in owned_cases:
            entries = CHAPTER_ENTRIES.get(case_name)
            if not entries:
                continue
            case = CASE_NAME_TO_CASE.get(case_name)
            if case is None:
                continue
            addresses = self._resolve_case_addresses(case)
            if addresses is None:
                continue
            first_addresses.append(addresses[0])
        if not first_addresses:
            return 0
        current_values = self.pine.batch_read_int8(first_addresses)
        writes = [
            (address, MissionFlag.UNLOCKED)
            for address, value in zip(first_addresses, current_values)
            if value in (MissionFlag.DISABLED, MissionFlag.ENABLED)
        ]
        if writes:
            self.pine.batch_write_int8(writes)
        return len(writes)

    def dump_chapter_table(self) -> list["ChapterTableRow"]:
        """For /mission_table: each slot's task count against the tasks expected for the cases found in it."""
        slots = resolve_chapter_table(self.pine, self.table_base)
        rows = []
        for slot, (pointer, count) in sorted(slots.items()):
            labels = self.pine.batch_read_int32([pointer + i * 0x60 + 0x3C for i in range(count)])
            names = list(dict.fromkeys(CASE_LABELS[label] for label in labels if label in CASE_LABELS))
            expected = sum(len(CHAPTER_ENTRIES.get(name, ())) for name in names)
            rows.append(ChapterTableRow(slot, count, " / ".join(names) or None,
                                        expected if names else None, expected == count if names else None))
        return rows

    def __repr__(self) -> str:
        seen = sum(self.completed.values())
        return f"MissionInventory(completed={seen}/{len(self.completed)})"

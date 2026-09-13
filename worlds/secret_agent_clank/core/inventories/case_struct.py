"""Batch reader/writer for the case-unlock table's exact layout (see
core/address_maps/ps2.py's CASE_UNLOCK_TABLE_OFFSETS) -- 31 slots,
offsets CONFIRMED live relative to the table's own start (slot 1). Each
slot is 0 (LOCKED) or 3 (UNLOCKED), same as CaseUnlockState.

Which SACCase each slot belongs to is CASE_UNLOCK_TABLE_SLOT_TO_CASE
(CONFIRMED live: slot = case_id + 1, slot 1 reserved/unused -- see that
dict's own comment) -- this class works purely by raw slot index/offset
regardless of that mapping, so it doubles as the tool used to identify
new slots by observing the in-game effect of write_slot().

Like CaseUnlockInventory (core/case_unlocks.py), this class re-derives
the table's start position fresh every call from whichever case is
CURRENTLY loaded (its own CASE_UNLOCK_BASE_ADDRESSES anchor minus that
case's own offset into the table) rather than assuming its anchor sits at
the table's start -- the table's absolute location moves on every case
transition (see case_unlocks.py's module docstring), and only Boltaire
Museum's anchor (slot 2) happens to have offset 0, so treating anchor +
offset as an absolute address only worked out for that one case."""
from typing import TYPE_CHECKING

from ...constants.planets import CASE_ID_TO_CASE
from ..address_maps import (
    CASE_NAME_TO_UNLOCK_SLOT,
    CASE_UNLOCK_BASE_ADDRESSES,
    CASE_UNLOCK_TABLE_OFFSETS,
    CASE_UNLOCK_TABLE_SLOT_TO_CASE,
)

if TYPE_CHECKING:
    from ...pypine import Pine


class CaseStructInventory:
    """Batch reads/writes every slot in CASE_UNLOCK_TABLE_OFFSETS, for
    whichever case is currently loaded. A no-op wherever the current case
    is unknown or its CASE_UNLOCK_BASE_ADDRESSES anchor isn't confirmed
    live yet."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine

    def _resolve_table_start(self, current_case_id: "int | None") -> int:
        """The address of slot 1 (CASE_UNLOCK_TABLE_OFFSETS[0]) for
        whichever case is CURRENTLY loaded -- i.e. the base every other
        slot's address in this table is computed relative to."""
        current_case = CASE_ID_TO_CASE.get(current_case_id) if current_case_id is not None else None
        if current_case is None:
            return 0
        anchor = CASE_UNLOCK_BASE_ADDRESSES.get(current_case.name, 0)
        if not anchor:
            return 0
        current_slot = CASE_NAME_TO_UNLOCK_SLOT.get(current_case.name)
        if current_slot is None:
            return 0
        return anchor - CASE_UNLOCK_TABLE_OFFSETS[current_slot - 1]

    def read_all(self, current_case_id: "int | None") -> dict[int, int]:
        """Batch-read every slot, keyed by its 1-indexed position in
        CASE_UNLOCK_TABLE_OFFSETS -- empty if the current case is unknown
        or its anchor isn't confirmed live yet."""
        table_start = self._resolve_table_start(current_case_id)
        if not table_start:
            return {}
        addresses = [table_start + offset for offset in CASE_UNLOCK_TABLE_OFFSETS]
        raw_values = self.pine.batch_read_int8(addresses)
        return dict(enumerate(raw_values, start=1))

    def write_slot(self, current_case_id: "int | None", slot: int, value: int) -> bool:
        """Debug/testing helper -- write a single slot by its 1-indexed
        position in CASE_UNLOCK_TABLE_OFFSETS, for narrowing down which
        case it belongs to by observing the in-game effect (typically 0 =
        LOCKED or 3 = UNLOCKED, see CaseUnlockState). Returns False
        (no-op) if the current case is unknown/unconfirmed or slot is out
        of range."""
        if not 1 <= slot <= len(CASE_UNLOCK_TABLE_OFFSETS):
            return False
        table_start = self._resolve_table_start(current_case_id)
        if not table_start:
            return False
        self.pine.write_int8(table_start + CASE_UNLOCK_TABLE_OFFSETS[slot - 1], value)
        return True

    def slot_case_name(self, slot: int) -> "str | None":
        """The SACCase name already identified for this slot, if any --
        see CASE_UNLOCK_TABLE_SLOT_TO_CASE."""
        return CASE_UNLOCK_TABLE_SLOT_TO_CASE.get(slot)

    def __repr__(self) -> str:
        identified = len(CASE_UNLOCK_TABLE_SLOT_TO_CASE)
        total = len(CASE_UNLOCK_TABLE_OFFSETS)
        return f"CaseStructInventory(slots={total}, identified={identified})"

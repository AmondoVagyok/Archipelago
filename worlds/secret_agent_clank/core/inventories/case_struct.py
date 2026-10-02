"""Diagnostic reader for the 31-slot case-unlock table (offsets confirmed live, relative to slot 1)."""
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
    """Reads every slot in CASE_UNLOCK_TABLE_OFFSETS for the currently loaded case."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine

    def _resolve_table_start(self, current_case_id: "int | None") -> int:
        """Address of slot 1 for the currently loaded case, or 0 if its anchor is unknown."""
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
        """Read every slot, keyed by 1-based position; empty if the table can't be located."""
        table_start = self._resolve_table_start(current_case_id)
        if not table_start:
            return {}
        addresses = [table_start + offset for offset in CASE_UNLOCK_TABLE_OFFSETS]
        raw_values = self.pine.batch_read_int8(addresses)
        return dict(enumerate(raw_values, start=1))

    def slot_case_name(self, slot: int) -> "str | None":
        """The case identified for this slot, if any."""
        return CASE_UNLOCK_TABLE_SLOT_TO_CASE.get(slot)

    def __repr__(self) -> str:
        identified = len(CASE_UNLOCK_TABLE_SLOT_TO_CASE)
        total = len(CASE_UNLOCK_TABLE_OFFSETS)
        return f"CaseStructInventory(slots={total}, identified={identified})"

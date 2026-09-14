"""Native keycard flag 0xAA: red bit 0, blue bit 1, yellow bit 2."""
from dataclasses import dataclass

from .planets import SACCases
from .types import CaseStructure, group_by_case


@dataclass(frozen=True)
class SACKeycards:
    RED_KEYCARD = "Red Keycard"
    BLUE_KEYCARD = "Blue Keycard"
    YELLOW_KEYCARD = "Yellow Keycard"


_CATEGORY = "Keycard"

KEYCARDS: tuple[CaseStructure, ...] = (
    CaseStructure(SACCases.ASYANICA_ROOFTOPS, SACKeycards.RED_KEYCARD, _CATEGORY),
    CaseStructure(SACCases.INSIDE_THE_A_EYE, SACKeycards.BLUE_KEYCARD, _CATEGORY),
    CaseStructure(SACCases.SAINT_QWARK, SACKeycards.YELLOW_KEYCARD, _CATEGORY),
)

KEYCARDS_BY_CASE: dict[str, tuple[str, ...]] = group_by_case(
    tuple(entry for entry in KEYCARDS if entry.case_name != "TODO")
)

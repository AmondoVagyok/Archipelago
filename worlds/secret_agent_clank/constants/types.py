"""CaseStructure: a single per-case, bit-flag-tracked location -- pairs a short event title with its Case, memory address and completion bit."""
from dataclasses import dataclass

from .planets import CASE_NAME_TO_OPERATIVE


@dataclass(frozen=True)
class CaseStructure:
    case_name: str          # SACCases constant (or "TODO" if not yet known)
    event_name: str         # short title -- the one part every entry must hand-type
    category: str = ""      # e.g. "Gadgetbot Challenge", "Skill Point" -- "" for missions/cutscenes
    event_flag: int = 0      # bitmask within event_address's byte; 0 = not confirmed live yet
    event_address: int = 0   # 0 = not confirmed live yet

    @property
    def operative(self) -> str:
        return CASE_NAME_TO_OPERATIVE.get(self.case_name, self.case_name)

    def check_flag(self, flag_value: int) -> bool:
        """Check if this event's completion bit is set in the given byte."""
        return bool(flag_value & self.event_flag)

    def __str__(self) -> str:
        middle = f"{self.category}: " if self.category else ""
        return f"{self.operative}: {self.case_name}: {middle}{self.event_name}"


def group_by_case(entries: tuple[CaseStructure, ...]) -> dict[str, tuple[str, ...]]:
    """Group a flat tuple of CaseStructure entries into case_name -> tuple of full display names, in declaration order -- the shape locations.py's *_BY_CASE loops expect (see e.g."""
    by_case: dict[str, list[str]] = {}
    for entry in entries:
        by_case.setdefault(entry.case_name, []).append(str(entry))
    return {case: tuple(names) for case, names in by_case.items()}

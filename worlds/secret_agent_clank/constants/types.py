"""Shared record types: Case (one per case) and CaseStructure (one flag-tracked location)."""
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .missions import SACMissionEntry


@dataclass(frozen=True)
class SACTags:
    """Values for CaseStructure.category."""

    ALIEN_CODE = "Alien Code"
    GADGETBOT_CHALLENGE = "Gadgetbot Challenge"
    KEYCARD = "Keycard"
    RATCHET_CHALLENGE = "Ratchet Challenge"
    SKILL_POINT = "Skill Point"
    SPECIAL_CHALLENGE = "Special Challenge"
    TITANIUM_BOLT = "T-Bolt"


@dataclass(frozen=True)
class Case:
    """One case, plus properties listing its locations and items in each category.

    The properties import their category modules lazily: those modules import
    this one (via planets.py), so importing them at module level would cycle.
    """
    name: str
    case_id: int
    planet: str       # SACPlanets constant
    operative: str    # SACOperatives constant
    menu_id: "int | None" = None

    @property
    def missions(self) -> "tuple[SACMissionEntry, ...]":
        from .missions import CHAPTER_ENTRIES
        return tuple(CHAPTER_ENTRIES.get(self.name, ()))

    @property
    def cutscenes(self) -> "tuple[CaseStructure, ...]":
        from .cutscenes import CUTSCENES
        return tuple(entry for entry in CUTSCENES if entry.case_name == self.name)

    @property
    def ratchet_challenges(self) -> "tuple[CaseStructure, ...]":
        from .ratchet_challenges import RATCHET_CHALLENGES
        return tuple(entry for entry in RATCHET_CHALLENGES if entry.case_name == self.name)

    @property
    def gadgetbot_challenges(self) -> "tuple[CaseStructure, ...]":
        from .gadgetbot_challenges import GADGETBOT_CHALLENGES
        return tuple(entry for entry in GADGETBOT_CHALLENGES if entry.case_name == self.name)

    @property
    def special_challenges(self) -> "tuple[CaseStructure, ...]":
        from .special_challenges import SPECIAL_CHALLENGES
        return tuple(entry for entry in SPECIAL_CHALLENGES if entry.case_name == self.name)

    @property
    def skill_points(self) -> "tuple[CaseStructure, ...]":
        from .skillpoints import SKILL_POINTS
        return tuple(entry for entry in SKILL_POINTS if entry.case_name == self.name)

    @property
    def titanium_bolts(self) -> "tuple[CaseStructure, ...]":
        from .titanium_bolts import TITANIUM_BOLT_ENTRIES
        return tuple(entry for entry in TITANIUM_BOLT_ENTRIES.values() if entry.case_name == self.name)

    @property
    def keycards(self) -> "tuple[CaseStructure, ...]":
        from .keycards import KEYCARDS
        return tuple(entry for entry in KEYCARDS if entry.case_name == self.name)

    @property
    def alien_codes(self) -> "tuple[CaseStructure, ...]":
        from .alien_codes import ALIEN_CODES
        return tuple(entry for entry in ALIEN_CODES if entry.case_name == self.name)

    @property
    def weapons(self) -> tuple[str, ...]:
        from .weapons import WEAPONS_BY_CASE
        return WEAPONS_BY_CASE.get(self.name, ())

    @property
    def gadgets(self) -> tuple[str, ...]:
        from .weapons import GADGETS_BY_CASE
        return GADGETS_BY_CASE.get(self.name, ())


@dataclass(frozen=True)
class CaseStructure:
    case_name: str          # SACCases constant
    event_name: str         # short title
    category: str = ""      # e.g. "Gadgetbot Challenge", "Skill Point" -- "" for missions/cutscenes
    event_flag: int = 0      # bitmask within event_address's byte; 0 = not confirmed live yet
    event_address: int = 0   # 0 = not confirmed live yet
    # AP location name, attached by with_display_names(); None uses __str__'s generic form.
    display_name: "str | None" = None

    @property
    def operative(self) -> str:
        from .planets import CASE_NAME_TO_OPERATIVE
        return CASE_NAME_TO_OPERATIVE.get(self.case_name, self.case_name)

    def check_flag(self, flag_value: int) -> bool:
        """Check if this event's completion bit is set in the given byte."""
        return bool(flag_value & self.event_flag)

    def __str__(self) -> str:
        if self.display_name is not None:
            return self.display_name
        middle = f"{self.category}: " if self.category else ""
        return f"{self.operative}: {self.case_name}: {middle}{self.event_name}"


def with_display_names(
    entries: tuple[CaseStructure, ...], names_cls: type,
) -> tuple[CaseStructure, ...]:
    """Attach AP location names from names_cls, pairing its attributes with entries by declaration order."""
    names = [value for name, value in vars(names_cls).items() if not name.startswith("_")]
    if len(names) != len(entries):
        raise ValueError(
            f"{names_cls.__name__} has {len(names)} entries, but {len(entries)} CaseStructure entries exist")
    return tuple(replace(entry, display_name=name) for entry, name in zip(entries, names))


def group_by_case(entries: tuple[CaseStructure, ...]) -> dict[str, tuple[str, ...]]:
    """Group entries into case_name -> location names, in declaration order."""
    by_case: dict[str, list[str]] = {}
    for entry in entries:
        by_case.setdefault(entry.case_name, []).append(str(entry))
    return {case: tuple(names) for case, names in by_case.items()}

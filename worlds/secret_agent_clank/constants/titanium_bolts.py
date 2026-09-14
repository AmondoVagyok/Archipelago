"""Native titanium bolt IDs (one-based), from the USA game's count table."""
from dataclasses import dataclass

from .planets import SACCases
from .types import CaseStructure, group_by_case

_CATEGORY = "T-Bolt"

TITANIUM_BOLT_CASES = {
    1: (SACCases.BOLTAIRE_MUSEUM, 2),
    3: (SACCases.MAX_SECURITY_CELLS, 1),
    4: (SACCases.ASYANICA_ROOFTOPS, 1),
    9: (SACCases.THE_MESS_HALL, 1),
    10: (SACCases.AZCOTAL_ALLEY, 3),
    11: (SACCases.GONDOLA_ASCENT, 1),
    13: (SACCases.HIGH_ROLLERS_CASINO, 1),
    14: (SACCases.THE_EXERCISE_YARD, 1),
    16: (SACCases.VENANTONIO_LABS, 2),
    19: (SACCases.GALACTIC_BOLT_RESERVE, 3),
    21: (SACCases.THE_SHOWERS, 1),
    22: (SACCases.SPACESHIP_GRAVEYARD, 4),
    25: (SACCases.PRISON_BREAKOUT, 1),
    29: (SACCases.UNDERWATER_BUNKER, 1),
}
# Flavor-text overrides for specific bolts -- (module, index) -> the actual
# in-game hint/description, in place of the plain numeric index. Anything
# not listed here just uses str(index), as before.
TITANIUM_BOLT_DESCRIPTIONS: dict[tuple[int, int], str] = {
    (1, 1): "JetBoot around the pillar",
    (1, 2): "Jump over the railings",
    (3, 1): "Complete Mega Challenge",
}

TITANIUM_BOLT_ENTRIES = {
    (module, index): CaseStructure(case, TITANIUM_BOLT_DESCRIPTIONS.get((module, index), str(index)), _CATEGORY)
    for module, (case, count) in TITANIUM_BOLT_CASES.items()
    for index in range(1, count + 1)
}

# Case name -> its titanium bolts' full display names, same group_by_case
# shape as SKILL_POINTS_BY_CASE/ALIEN_CODES_BY_CASE -- lets rules/<case>.py
# reference these locations by constant instead of hand-typing them.
TITANIUM_BOLTS_BY_CASE: dict[str, tuple[str, ...]] = group_by_case(tuple(TITANIUM_BOLT_ENTRIES.values()))


@dataclass(frozen=True)
class SACTitaniumBoltLocations:
    """One named constant per titanium bolt location -- each value is the exact full display name TITANIUM_BOLT_ENTRIES above builds via CaseStructure.__str__, spelled out here so rules/<case>.py can reference an individual location directly -- same one-name-per-location layout as constants/weapons.py's SACRatchetWeapons."""

    BOLTAIRE_MUSEUM_1 = "Clank: Boltaire Museum: T-Bolt: JetBoot around the pillar"
    BOLTAIRE_MUSEUM_2 = "Clank: Boltaire Museum: T-Bolt: Jump over the railings"
    MAX_SECURITY_CELLS_1 = "Ratchet: Max-Security Cells: T-Bolt: Complete Mega Challenge"
    ASYANICA_ROOFTOPS_1 = "Clank: Asyanica Rooftops: T-Bolt: 1"
    THE_MESS_HALL_1 = "Ratchet: The Mess Hall: T-Bolt: 1"
    AZCOTAL_ALLEY_1 = "Clank: Azcotal Alley: T-Bolt: 1"
    AZCOTAL_ALLEY_2 = "Clank: Azcotal Alley: T-Bolt: 2"
    AZCOTAL_ALLEY_3 = "Clank: Azcotal Alley: T-Bolt: 3"
    GONDOLA_ASCENT_1 = "Clank: Gondola Ascent: T-Bolt: 1"
    HIGH_ROLLERS_CASINO_1 = "Clank: High-Rollers Casino: T-Bolt: 1"
    THE_EXERCISE_YARD_1 = "Ratchet: The Exercise Yard: T-Bolt: 1"
    VENANTONIO_LABS_1 = "Clank: Venantonio Labs: T-Bolt: 1"
    VENANTONIO_LABS_2 = "Clank: Venantonio Labs: T-Bolt: 2"
    GALACTIC_BOLT_RESERVE_1 = "Clank: Galactic Bolt Reserve: T-Bolt: 1"
    GALACTIC_BOLT_RESERVE_2 = "Clank: Galactic Bolt Reserve: T-Bolt: 2"
    GALACTIC_BOLT_RESERVE_3 = "Clank: Galactic Bolt Reserve: T-Bolt: 3"
    THE_SHOWERS_1 = "Ratchet: The Showers: T-Bolt: 1"
    SPACESHIP_GRAVEYARD_1 = "Clank: Spaceship Graveyard: T-Bolt: 1"
    SPACESHIP_GRAVEYARD_2 = "Clank: Spaceship Graveyard: T-Bolt: 2"
    SPACESHIP_GRAVEYARD_3 = "Clank: Spaceship Graveyard: T-Bolt: 3"
    SPACESHIP_GRAVEYARD_4 = "Clank: Spaceship Graveyard: T-Bolt: 4"
    PRISON_BREAKOUT_1 = "Ratchet: Prison Breakout!: T-Bolt: 1"
    UNDERWATER_BUNKER_1 = "Clank: Underwater Bunker: T-Bolt: 1"

assert {v for k, v in vars(SACTitaniumBoltLocations).items() if not k.startswith("_")} == {
    str(entry) for entry in TITANIUM_BOLT_ENTRIES.values()
}, "SACTitaniumBoltLocations drifted out of sync with TITANIUM_BOLT_ENTRIES -- regenerate its literals"

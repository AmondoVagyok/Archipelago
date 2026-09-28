"""Every location in Klunk's Lair, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACClankWeapons,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACRatchetWeapons,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.HYDRANO
_CASE = SACCases.KLUNKS_LAIR

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.KLUNKS_LAIR_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_829_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.KLUNKS_LAIR_ALL_THE_MARBLES,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_829_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.KLUNKS_LAIR_TURN_THE_TABLES,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_829_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.KLUNKS_LAIR_PRETTY_GOOD_LIKENESS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_829_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.KLUNKS_LAIR_ENTERE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_829_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.KLUNKS_LAIR_MID_FIGHT_CUTSCENE_FOR_ROBO_RATCHET,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_829_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.KLUNKS_LAIR_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_829_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.KLUNKS_LAIR_HIGH_IMPACT_GAMES_CUTSCENE_WITH_GIANT_CLANK,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_829_007,
        lambda world: True_(),
    ),
)

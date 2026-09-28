"""Every location in Suck and Jive, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.RIONOSIS
_CASE = SACCases.SUCK_AND_JIVE

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.SUCK_AND_JIVE_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_811_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.SUCK_AND_JIVE_QWARKOGRAPHY_THE_GAMBLIN_YEARS,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_811_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.SUCK_AND_JIVE_CARD_PICKUP,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_811_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.SUCK_AND_JIVE_DRESS_FOR_SUCCESS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_811_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.SUCK_AND_JIVE_DEFEAT_JACK_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_811_002,
        lambda world: True_(),
    ),
)

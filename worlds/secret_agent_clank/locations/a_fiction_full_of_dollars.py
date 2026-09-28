"""Every location in A Fiction Full Of Dollars, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.HYDRANO
_CASE = SACCases.A_FICTION_FULL_OF_DOLLARS

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.A_FICTION_FULL_OF_DOLLARS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_826_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.A_FICTION_FULL_OF_DOLLARS_QWARKOGRAPHY_CH_5,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_826_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_CLEANS_POOLS_TOO,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_826_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_PERFECT_MIRROR,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_826_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.A_FICTION_FULL_OF_DOLLARS_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_826_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.A_FICTION_FULL_OF_DOLLARS_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_826_003,
        lambda world: True_(),
    ),
)

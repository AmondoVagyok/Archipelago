"""Every location in Countess's Villa, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.GLACIARA
_CASE = SACCases.COUNTESS_VILLA

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.COUNTESS_VILLA_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_805_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.COUNTESS_VILLA_TANGO_OF_100_SORROWS,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_805_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.COUNTESS_VILLA_PERFECT_TANGO,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_805_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.COUNTESS_VILLA_ENTER_THE_MANSION,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_805_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.COUNTESS_VILLA_COMPLETE_DANCE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_805_003,
        lambda world: True_(),
    ),
)

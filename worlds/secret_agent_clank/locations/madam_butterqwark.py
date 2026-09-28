"""Every location in Madam Butterqwark, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.VENANTONIO
_CASE = SACCases.MADAM_BUTTERQWARK

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.MADAM_BUTTERQWARK_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_817_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.MADAM_BUTTERQWARK_QWARKOGRAPHY_CH_3,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_817_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.MADAM_BUTTERQWARK_TWINKLE_TOES,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_817_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.MADAM_BUTTERQWARK_MAGNUM_OPUS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_817_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.MADAM_BUTTERQWARK_SOLD_OUT,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_817_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.MADAM_BUTTERQWARK_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_817_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.MADAM_BUTTERQWARK_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_817_003,
        lambda world: True_(),
    ),
)

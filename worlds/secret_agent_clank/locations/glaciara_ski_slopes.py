"""Every location in Glaciara, Ski Slopes, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
    SACSpecialChallengeLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.GLACIARA
_CASE = SACCases.GLACIARA_SKI_SLOPES

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_VILLA_ESCAPE,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_807_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_BLACK_DIAMOND,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_807_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_GO_FOR_THE_GOLD,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_807_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.GLACIARA_SKI_SLOPES_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_807_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.GLACIARA_SKI_SLOPES_BLACK_DIAMOND_OF_DOOM,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_807_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.GLACIARA_SKI_SLOPES_PRO_BOARDING,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_807_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.GLACIARA_SKI_SLOPES_BLACK_DIAMOND,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_807_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.GLACIARA_SKI_SLOPES_SMOOTH_MOVES,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_807_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.GLACIARA_SKI_SLOPES_RINGLEADER,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_807_008,
        lambda world: True_(),
    ),
)

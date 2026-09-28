"""Every location in Venantonio Canals, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
    SACSpecialChallengeLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.VENANTONIO
_CASE = SACCases.VENANTONIO_CANALS

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_GREAT_ESCAPE,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_816_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_SPEEDBOATING,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_816_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_THREADING_THE_NEEDLE,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_816_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_CANALS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_816_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_CANALS_DANGER_OFF_STARBOARD,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_816_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.VENANTONIO_CANALS_POWER_JET_BOATING,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_816_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_CANALS_EVASIVE_MANEUVERS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_816_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_CANALS_DEEP_SIX,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_816_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_CANALS_WAKE_OF_DESTRUCTION,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_816_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.VENANTONIO_CANALS_RINGMASTER,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_816_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.VENANTONIO_CANALS_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_816_006,
        lambda world: True_(),
    ),
)

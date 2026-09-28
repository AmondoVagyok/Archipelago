"""Every location in Dam's Edge, Hydrano, each carrying its planet, case and access rule."""
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

_PLANET = SACPlanets.HYDRANO
_CASE = SACCases.DAMS_EDGE_HYDRANO

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_CHASING_A_LEAD,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_825_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_RUSH_HOUR,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_825_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_DRIVING_TEST,
        _PLANET,
        _CASE,
        SACLocationType.SPECIAL_CHALLENGE,
        77_825_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.DAMS_EDGE_HYDRANO_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_825_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.DAMS_EDGE_HYDRANO_SHIP_S_SIGNAL,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_825_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.DAMS_EDGE_HYDRANO_FOLLOW_THAT_CAR,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_825_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.DAMS_EDGE_HYDRANO_THE_DRIFT_KING,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_825_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.DAMS_EDGE_HYDRANO_YEEE_HAAAAAW,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_825_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.DAMS_EDGE_HYDRANO_OFFENSIVE_DRIVER,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_825_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.DAMS_EDGE_HYDRANO_SLIPPERY_SLOPE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_825_011,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.DAMS_EDGE_HYDRANO_RING_AROUND_THE_ROSIE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_825_012,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.DAMS_EDGE_HYDRANO_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_825_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.DAMS_EDGE_HYDRANO_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_825_008,
        lambda world: True_(),
    ),
)

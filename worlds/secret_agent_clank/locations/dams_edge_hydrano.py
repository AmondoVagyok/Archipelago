"""Dam's Edge, Hydrano: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACSkillPointLocations,
    SACSpecialChallengeLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.DAMS_EDGE_HYDRANO, (
    SACLocation(SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_CHASING_A_LEAD,
                SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_RUSH_HOUR, SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_DRIVING_TEST, SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACMissionLocations.DAMS_EDGE_HYDRANO_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.DAMS_EDGE_HYDRANO_SHIP_S_SIGNAL, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.DAMS_EDGE_HYDRANO_FOLLOW_THAT_CAR, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.DAMS_EDGE_HYDRANO_THE_DRIFT_KING, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.DAMS_EDGE_HYDRANO_YEEE_HAAAAAW, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.DAMS_EDGE_HYDRANO_OFFENSIVE_DRIVER, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.DAMS_EDGE_HYDRANO_SLIPPERY_SLOPE, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.DAMS_EDGE_HYDRANO_RING_AROUND_THE_ROSIE, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.DAMS_EDGE_HYDRANO_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.DAMS_EDGE_HYDRANO_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

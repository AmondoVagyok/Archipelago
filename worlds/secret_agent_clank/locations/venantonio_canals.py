"""Venantonio Canals: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACSkillPointLocations,
    SACSpecialChallengeLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.VENANTONIO_CANALS, (
    SACLocation(SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_GREAT_ESCAPE, SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_SPEEDBOATING, SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_THREADING_THE_NEEDLE,
                SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACMissionLocations.VENANTONIO_CANALS_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.VENANTONIO_CANALS_DANGER_OFF_STARBOARD, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.VENANTONIO_CANALS_POWER_JET_BOATING, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.VENANTONIO_CANALS_EVASIVE_MANEUVERS, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.VENANTONIO_CANALS_DEEP_SIX, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.VENANTONIO_CANALS_WAKE_OF_DESTRUCTION, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.VENANTONIO_CANALS_RINGMASTER, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.VENANTONIO_CANALS_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

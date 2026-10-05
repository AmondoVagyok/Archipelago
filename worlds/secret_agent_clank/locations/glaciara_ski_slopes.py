"""Glaciara, Ski Slopes: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACMissionLocations, SACSkillPointLocations, SACSpecialChallengeLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.GLACIARA_SKI_SLOPES, (
    SACLocation(SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_VILLA_ESCAPE,
                SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_BLACK_DIAMOND,
                SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_GO_FOR_THE_GOLD,
                SACLocationType.SPECIAL_CHALLENGE),
    SACLocation(SACMissionLocations.GLACIARA_SKI_SLOPES_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.GLACIARA_SKI_SLOPES_BLACK_DIAMOND_OF_DOOM, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.GLACIARA_SKI_SLOPES_PRO_BOARDING, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.GLACIARA_SKI_SLOPES_BLACK_DIAMOND, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.GLACIARA_SKI_SLOPES_SMOOTH_MOVES, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.GLACIARA_SKI_SLOPES_RINGLEADER, SACLocationType.SKILL_POINT),
))

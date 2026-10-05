"""Suck and Jive: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.SUCK_AND_JIVE, (
    SACLocation(SACMissionLocations.SUCK_AND_JIVE_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.SUCK_AND_JIVE_QWARKOGRAPHY_THE_GAMBLIN_YEARS, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.SUCK_AND_JIVE_CARD_PICKUP, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.SUCK_AND_JIVE_DRESS_FOR_SUCCESS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.SUCK_AND_JIVE_DEFEAT_JACK_CUTSCENE, SACLocationType.CUTSCENE),
))

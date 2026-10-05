"""Countess's Villa: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.COUNTESS_VILLA, (
    SACLocation(SACMissionLocations.COUNTESS_VILLA_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.COUNTESS_VILLA_TANGO_OF_100_SORROWS, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.COUNTESS_VILLA_PERFECT_TANGO, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.COUNTESS_VILLA_ENTER_THE_MANSION, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.COUNTESS_VILLA_COMPLETE_DANCE_CUTSCENE, SACLocationType.CUTSCENE),
))

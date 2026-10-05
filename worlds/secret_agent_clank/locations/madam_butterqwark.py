"""Madam Butterqwark: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.MADAM_BUTTERQWARK, (
    SACLocation(SACMissionLocations.MADAM_BUTTERQWARK_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.MADAM_BUTTERQWARK_QWARKOGRAPHY_CH_3, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.MADAM_BUTTERQWARK_TWINKLE_TOES, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.MADAM_BUTTERQWARK_MAGNUM_OPUS, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.MADAM_BUTTERQWARK_SOLD_OUT, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.MADAM_BUTTERQWARK_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.MADAM_BUTTERQWARK_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

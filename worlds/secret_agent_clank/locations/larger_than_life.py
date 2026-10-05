"""Larger Than Life: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.LARGER_THAN_LIFE, (
    SACLocation(SACMissionLocations.LARGER_THAN_LIFE_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.LARGER_THAN_LIFE_QWARKOGRAPHY_CH_1, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.LARGER_THAN_LIFE_INVERSE_NINJA_LAW, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.LARGER_THAN_LIFE_BLASTER_OVERLOAD, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.LARGER_THAN_LIFE_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.LARGER_THAN_LIFE_GODZILLA_LAZER_BEAM, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.LARGER_THAN_LIFE_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

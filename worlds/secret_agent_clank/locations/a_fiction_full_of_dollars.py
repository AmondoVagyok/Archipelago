"""A Fiction Full Of Dollars: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.A_FICTION_FULL_OF_DOLLARS, (
    SACLocation(SACMissionLocations.A_FICTION_FULL_OF_DOLLARS_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.A_FICTION_FULL_OF_DOLLARS_QWARKOGRAPHY_CH_5, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_CLEANS_POOLS_TOO, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_PERFECT_MIRROR, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.A_FICTION_FULL_OF_DOLLARS_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.A_FICTION_FULL_OF_DOLLARS_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

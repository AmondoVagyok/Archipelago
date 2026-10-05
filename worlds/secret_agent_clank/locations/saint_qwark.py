"""Saint Qwark: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACKeycardLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.SAINT_QWARK, (
    SACLocation(SACMissionLocations.SAINT_QWARK_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.SAINT_QWARK_QWARKOGRAPHY_CH_4, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.SAINT_QWARK_PUNCHY, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.SAINT_QWARK_SOUR_VICTORY, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.SAINT_QWARK_ENTERE_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACKeycardLocations.YELLOW_KEYCARD, SACLocationType.KEYCARD),
))

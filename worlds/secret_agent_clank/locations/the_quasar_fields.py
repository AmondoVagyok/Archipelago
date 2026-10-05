"""The Quasar Fields: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.THE_QUASAR_FIELDS, (
    SACLocation(SACMissionLocations.THE_QUASAR_FIELDS_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.THE_QUASAR_FIELDS_ESCAPE_THE_KUDZU, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.THE_QUASAR_FIELDS_MIN_MAXING, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.THE_QUASAR_FIELDS_KILL_THE_ROCK, SACLocationType.SKILL_POINT),
))

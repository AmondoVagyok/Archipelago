"""High Stakes Room: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.HIGH_STAKES_ROOM, (
    SACLocation(SACMissionLocations.HIGH_STAKES_ROOM_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.HIGH_STAKES_ROOM_HIGH_RISK_VS_HIGH_STAKES, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.HIGH_STAKES_ROOM_LUCKY_SEVENS, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.HIGH_STAKES_ROOM_GADGEBOT_STANDS_ALONE, SACLocationType.SKILL_POINT),
))

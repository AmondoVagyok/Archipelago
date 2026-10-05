"""The Showers: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.THE_SHOWERS, (
    SACLocation(SACRatchetChallengeLocations.THE_SHOWERS_NO_GOOD_DEED_GOES_UNPUNISHED,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_SHOWERS_COVER_YOUR_SHAME, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_SHOWERS_DIDNT_NEED_TO_SEE_THAT, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_SHOWERS_ITS_A_DRY_HEAT, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_SHOWERS_MEGA_CHALLENGE_SHOWER, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACTitaniumBoltLocations.THE_SHOWERS_1, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACMissionLocations.THE_SHOWERS_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.THE_SHOWERS_PLUMBING_TROUBLES, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.THE_SHOWERS_RUB_A_DUB_DEATH, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.THE_SHOWERS_RUBA_DUB_CLUB, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.THE_SHOWERS_MODESTY, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.THE_SHOWERS_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

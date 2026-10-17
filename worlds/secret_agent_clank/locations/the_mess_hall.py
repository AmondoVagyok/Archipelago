from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from ..rules import ProgressiveWrenchRule
from .model import CaseRegion, SACLocation, SACLocationType


REGION = CaseRegion(SACCases.THE_MESS_HALL, (
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_NAILS_FOR_BREAKFAST,
                SACLocationType.RATCHET_CHALLENGE, ProgressiveWrenchRule()),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_TYHRRANOID_RECYCLING,
                SACLocationType.RATCHET_CHALLENGE, ProgressiveWrenchRule()),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_ITS_RAINING_PHLEGM_HALLELUJAH,
                SACLocationType.RATCHET_CHALLENGE, ProgressiveWrenchRule()),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_MEATLOAF_TUESDAYS,
                SACLocationType.RATCHET_CHALLENGE, ProgressiveWrenchRule()),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_MEGA_CHALLENGE_CAFETERIA,
                SACLocationType.RATCHET_CHALLENGE, ProgressiveWrenchRule()),
    SACLocation(SACTitaniumBoltLocations.THE_MESS_HALL_1, SACLocationType.TITANIUM_BOLT, ProgressiveWrenchRule(), flag_bit=0),
    SACLocation(SACMissionLocations.THE_MESS_HALL_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.THE_MESS_HALL_NO_TIME_FOR_SECONDS, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.THE_MESS_HALL_THE_LUNCH_MENU_FOREVER, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.THE_MESS_HALL_EMPTY_THE_WARRENS, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.THE_MESS_HALL_ANTAEUS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.THE_MESS_HALL_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

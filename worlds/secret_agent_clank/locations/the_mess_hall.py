"""The Mess Hall: the case region and every location in it, with its access rule."""
from rule_builder.rules import Has, True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from ..items import PROGRESSIVE_WRENCH_ITEM_NAME
from .model import CaseRegion, SACLocation, SACLocationType


# Ratchet Challenges here are wrench-combo based -- with Progressive Wrench in the
# pool they need its first copy; otherwise the wrench is fully capable from the start.
def _wrench_rule(world):
    return Has(PROGRESSIVE_WRENCH_ITEM_NAME) if world.options.progressive_wrench else True_()


REGION = CaseRegion(SACCases.THE_MESS_HALL, (
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_NAILS_FOR_BREAKFAST,
                SACLocationType.RATCHET_CHALLENGE, _wrench_rule),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_TYHRRANOID_RECYCLING,
                SACLocationType.RATCHET_CHALLENGE, _wrench_rule),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_ITS_RAINING_PHLEGM_HALLELUJAH,
                SACLocationType.RATCHET_CHALLENGE, _wrench_rule),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_MEATLOAF_TUESDAYS,
                SACLocationType.RATCHET_CHALLENGE, _wrench_rule),
    SACLocation(SACRatchetChallengeLocations.THE_MESS_HALL_MEGA_CHALLENGE_CAFETERIA,
                SACLocationType.RATCHET_CHALLENGE, _wrench_rule),
    SACLocation(SACTitaniumBoltLocations.THE_MESS_HALL_1, SACLocationType.TITANIUM_BOLT, _wrench_rule),
    SACLocation(SACMissionLocations.THE_MESS_HALL_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.THE_MESS_HALL_NO_TIME_FOR_SECONDS, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.THE_MESS_HALL_THE_LUNCH_MENU_FOREVER, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.THE_MESS_HALL_EMPTY_THE_WARRENS, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.THE_MESS_HALL_ANTAEUS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.THE_MESS_HALL_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

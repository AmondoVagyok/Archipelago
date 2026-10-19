from rule_builder.rules import Has

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACRatchetWeapons,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
    SACVendor,
)
from ..rules import VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_VENDOR = VendorCaseRule(SACCases.PRISON_BREAKOUT)

REGION = CaseRegion(SACCases.PRISON_BREAKOUT, (
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_CATCH_AS_CATCH_CAN, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_AMOEBOID_ON_A_POLE, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_IRON_MAN, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_TRIPLE_THREAT, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_MEGA_CHALLENGE_BATTLE_ROYAL,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACTitaniumBoltLocations.PRISON_BREAKOUT_1, SACLocationType.TITANIUM_BOLT, flag_bit=0),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_THE_GREAT_ESCAPE, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_AND_NOW_JUSTICE_FOR_ALL, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.PRISON_BREAKOUT_WHIP_IT_GOOD, SACLocationType.SKILL_POINT,
                rule=Has(SACRatchetWeapons.PLASMAWHIP)),
    SACLocation(SACSkillPointLocations.PRISON_BREAKOUT_HANGING_JUDGE, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.PRISON_BREAKOUT_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACVendor.PRISON_BREAKOUT_SHOCK_ROCKET_TASER, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.PRISON_BREAKOUT_PLASMA_WHIP_FLAME_TRAILS, SACLocationType.MOD_VENDOR, _VENDOR),
))

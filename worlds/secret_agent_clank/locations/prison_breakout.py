"""Prison Breakout!: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.PRISON_BREAKOUT, (
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_CATCH_AS_CATCH_CAN, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_AMOEBOID_ON_A_POLE, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_IRON_MAN, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_TRIPLE_THREAT, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.PRISON_BREAKOUT_MEGA_CHALLENGE_BATTLE_ROYAL,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACTitaniumBoltLocations.PRISON_BREAKOUT_1, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_THE_GREAT_ESCAPE, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.PRISON_BREAKOUT_AND_NOW_JUSTICE_FOR_ALL, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.PRISON_BREAKOUT_WHIP_IT_GOOD, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.PRISON_BREAKOUT_HANGING_JUDGE, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.PRISON_BREAKOUT_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

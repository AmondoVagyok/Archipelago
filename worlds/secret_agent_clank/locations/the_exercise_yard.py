"""The Exercise Yard: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.THE_EXERCISE_YARD, (
    SACLocation(SACRatchetChallengeLocations.THE_EXERCISE_YARD_LAST_ONE_PICKED_FOR_DODGEBALL,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_EXERCISE_YARD_STEEL_IS_STEEL, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_EXERCISE_YARD_PUMPING_IRON_MOLTEN_IRON,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_EXERCISE_YARD_GREAT_BALLS_OF_FIRE, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.THE_EXERCISE_YARD_MEGA_CHALLENGE_PRISON_YARD,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACTitaniumBoltLocations.THE_EXERCISE_YARD_1, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACMissionLocations.THE_EXERCISE_YARD_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.THE_EXERCISE_YARD_AND_THE_PASSWORD_IS, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.THE_EXERCISE_YARD_FIGHT_FOR_SLIM, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.THE_EXERCISE_YARD_INDIAN_BURN, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.THE_EXERCISE_YARD_LAW_CANT_TOUCH_ME, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.THE_EXERCISE_YARD_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
))

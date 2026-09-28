"""Every location in The Exercise Yard, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.PRISON_PLANET
_CASE = SACCases.THE_EXERCISE_YARD

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACRatchetChallengeLocations.THE_EXERCISE_YARD_LAST_ONE_PICKED_FOR_DODGEBALL,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_813_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_EXERCISE_YARD_STEEL_IS_STEEL,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_813_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_EXERCISE_YARD_PUMPING_IRON_MOLTEN_IRON,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_813_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_EXERCISE_YARD_GREAT_BALLS_OF_FIRE,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_813_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_EXERCISE_YARD_MEGA_CHALLENGE_PRISON_YARD,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_813_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACTitaniumBoltLocations.THE_EXERCISE_YARD_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_813_901,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_EXERCISE_YARD_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_813_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_EXERCISE_YARD_AND_THE_PASSWORD_IS,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_813_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_EXERCISE_YARD_FIGHT_FOR_SLIM,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_813_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_EXERCISE_YARD_INDIAN_BURN,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_813_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_EXERCISE_YARD_LAW_CANT_TOUCH_ME,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_813_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.THE_EXERCISE_YARD_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_813_008,
        lambda world: True_(),
    ),
)

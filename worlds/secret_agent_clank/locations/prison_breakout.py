"""Every location in Prison Breakout!, each carrying its planet, case and access rule."""
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
_CASE = SACCases.PRISON_BREAKOUT

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACRatchetChallengeLocations.PRISON_BREAKOUT_CATCH_AS_CATCH_CAN,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_824_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.PRISON_BREAKOUT_AMOEBOID_ON_A_POLE,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_824_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.PRISON_BREAKOUT_IRON_MAN,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_824_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.PRISON_BREAKOUT_TRIPLE_THREAT,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_824_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.PRISON_BREAKOUT_MEGA_CHALLENGE_BATTLE_ROYAL,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_824_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACTitaniumBoltLocations.PRISON_BREAKOUT_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_824_901,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.PRISON_BREAKOUT_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_824_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.PRISON_BREAKOUT_THE_GREAT_ESCAPE,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_824_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.PRISON_BREAKOUT_AND_NOW_JUSTICE_FOR_ALL,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_824_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.PRISON_BREAKOUT_WHIP_IT_GOOD,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_824_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.PRISON_BREAKOUT_HANGING_JUDGE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_824_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.PRISON_BREAKOUT_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_824_008,
        lambda world: True_(),
    ),
)

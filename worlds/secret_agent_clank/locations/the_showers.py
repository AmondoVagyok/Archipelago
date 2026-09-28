"""Every location in The Showers, each carrying its planet, case and access rule."""
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
_CASE = SACCases.THE_SHOWERS

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACRatchetChallengeLocations.THE_SHOWERS_NO_GOOD_DEED_GOES_UNPUNISHED,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_820_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_SHOWERS_COVER_YOUR_SHAME,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_820_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_SHOWERS_DIDNT_NEED_TO_SEE_THAT,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_820_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_SHOWERS_ITS_A_DRY_HEAT,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_820_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_SHOWERS_MEGA_CHALLENGE_SHOWER,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_820_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACTitaniumBoltLocations.THE_SHOWERS_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_820_901,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_SHOWERS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_820_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_SHOWERS_PLUMBING_TROUBLES,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_820_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_SHOWERS_RUB_A_DUB_DEATH,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_820_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_SHOWERS_RUBA_DUB_CLUB,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_820_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_SHOWERS_MODESTY,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_820_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.THE_SHOWERS_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_820_008,
        lambda world: True_(),
    ),
)

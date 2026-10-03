"""Every location in Max-Security Cells, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPickups,
    SACPlanets,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.PRISON_PLANET
_CASE = SACCases.MAX_SECURITY_CELLS

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACPickups.MAX_SECURITY_CELLS_SHARDGUN,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_WEAPON,
        77_802_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACPickups.MAX_SECURITY_CELLS_WALLOPER,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_WEAPON,
        77_802_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.MAX_SECURITY_CELLS_KARMIC_BREAKDOWN,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_802_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.MAX_SECURITY_CELLS_NO_SHELTER,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_802_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.MAX_SECURITY_CELLS_PAST_DUE,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_802_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.MAX_SECURITY_CELLS_SPEAK_SOFTLY_AND,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_802_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACRatchetChallengeLocations.MAX_SECURITY_CELLS_MEGA_CHALLENGE_CELLBLOCK,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_802_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACTitaniumBoltLocations.MAX_SECURITY_CELLS_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_802_901,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.MAX_SECURITY_CELLS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_802_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.MAX_SECURITY_CELLS_LIFE_IN_PRISON,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_802_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.MAX_SECURITY_CELLS_CONSECUTIVE_LIFE_SENTENCES,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_802_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.MAX_SECURITY_CELLS_STAINLESS_STEEL,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_802_011,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.MAX_SECURITY_CELLS_PLAYING_WITH_FIRE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_802_012,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.MAX_SECURITY_CELLS_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_802_010,
        lambda world: True_(),
    ),
)

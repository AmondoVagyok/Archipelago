"""Every location in Bulkhead Lock, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACGadgetbotChallengeLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.FORT_SPROCKET
_CASE = SACCases.BULKHEAD_LOCK

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACGadgetbotChallengeLocations.BULKHEAD_LOCK_KNOCKIN_ON_KLUNKS_DOOR,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_827_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.BULKHEAD_LOCK_MISSION_POSSIBLE,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_827_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.BULKHEAD_LOCK_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_827_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.BULKHEAD_LOCK_UNDERWATER_BASE,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_827_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.BULKHEAD_LOCK_LOCKED_DOOR,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_827_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.BULKHEAD_LOCK_INSULT_TO_INJURY,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_827_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.BULKHEAD_LOCK_CEREAL_DECODER_RING,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_827_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.BULKHEAD_LOCK_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_827_006,
        lambda world: True_(),
    ),
)

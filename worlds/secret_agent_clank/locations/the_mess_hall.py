"""Every location in The Mess Hall, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from ..items import PROGRESSIVE_WRENCH_ITEM_NAME
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.PRISON_PLANET
_CASE = SACCases.THE_MESS_HALL


# Ratchet Challenges here are wrench-combo based -- with Progressive Wrench in the
# pool they need its first copy; otherwise the wrench is fully capable from the start.
def _wrench_rule(world):
    return Has(PROGRESSIVE_WRENCH_ITEM_NAME) if world.options.progressive_wrench else True_()


LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACRatchetChallengeLocations.THE_MESS_HALL_NAILS_FOR_BREAKFAST,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_808_000,
        _wrench_rule,
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_MESS_HALL_TYHRRANOID_RECYCLING,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_808_001,
        _wrench_rule,
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_MESS_HALL_ITS_RAINING_PHLEGM_HALLELUJAH,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_808_002,
        _wrench_rule,
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_MESS_HALL_MEATLOAF_TUESDAYS,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_808_003,
        _wrench_rule,
    ),
    SACLocation(
        SACRatchetChallengeLocations.THE_MESS_HALL_MEGA_CHALLENGE_CAFETERIA,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_CHALLENGE,
        77_808_004,
        _wrench_rule,
    ),
    SACLocation(
        SACTitaniumBoltLocations.THE_MESS_HALL_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_808_901,
        _wrench_rule,
    ),
    SACLocation(
        SACMissionLocations.THE_MESS_HALL_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_808_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_MESS_HALL_NO_TIME_FOR_SECONDS,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_808_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_MESS_HALL_THE_LUNCH_MENU_FOREVER,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_808_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_MESS_HALL_EMPTY_THE_WARRENS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_808_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_MESS_HALL_ANTAEUS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_808_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.THE_MESS_HALL_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_808_008,
        lambda world: True_(),
    ),
)

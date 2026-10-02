"""Every location in Rooftop Deathtrap, each carrying its planet, case and access rule."""
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

_PLANET = SACPlanets.ASYANICA
_CASE = SACCases.ROOFTOP_DEATHTRAP

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_RESCUE_CLANK,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_803_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_WORKING_DOWN,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_803_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_GREAT_DIVIDE,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_803_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.ROOFTOP_DEATHTRAP_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_803_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.ROOFTOP_DEATHTRAP_GET_A_CLUE,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_803_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.ROOFTOP_DEATHTRAP_FREE_AGENT_CLANK,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_803_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.ROOFTOP_DEATHTRAP_THE_HALLS_OF_ASYANICA,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_803_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.ROOFTOP_DEATHTRAP_SPEED_DEMON,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_803_012,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.ROOFTOP_DEATHTRAP_PERFECT_CHROME_FINISH,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_803_013,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.ROOFTOP_DEATHTRAP_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_803_010,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.ROOFTOP_DEATHTRAP_RESCURE_CLANK_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_803_011,
        lambda world: True_(),
    ),
)

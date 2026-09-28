"""Every location in Larger Than Life, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.ASYANICA
_CASE = SACCases.LARGER_THAN_LIFE

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.LARGER_THAN_LIFE_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_804_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.LARGER_THAN_LIFE_QWARKOGRAPHY_CH_1,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_804_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.LARGER_THAN_LIFE_INVERSE_NINJA_LAW,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_804_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.LARGER_THAN_LIFE_BLASTER_OVERLOAD,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_804_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.LARGER_THAN_LIFE_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_804_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.LARGER_THAN_LIFE_GODZILLA_LAZER_BEAM,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_804_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.LARGER_THAN_LIFE_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_804_004,
        lambda world: True_(),
    ),
)

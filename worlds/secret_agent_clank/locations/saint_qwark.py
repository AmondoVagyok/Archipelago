"""Every location in Saint Qwark, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACKeycardLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.SPACESHIP_GRAVEYARD
_CASE = SACCases.SAINT_QWARK

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.SAINT_QWARK_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_822_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.SAINT_QWARK_QWARKOGRAPHY_CH_4,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_822_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.SAINT_QWARK_PUNCHY,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_822_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.SAINT_QWARK_SOUR_VICTORY,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_822_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.SAINT_QWARK_ENTERE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_822_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACKeycardLocations.YELLOW_KEYCARD,
        _PLANET,
        _CASE,
        SACLocationType.KEYCARD,
        77_822_005,
    ),
)

"""Every location in The Quasar Fields, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import SACCases, SACMissionLocations, SACPlanets, SACSkillPointLocations
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.SPACESHIP_GRAVEYARD
_CASE = SACCases.THE_QUASAR_FIELDS

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.THE_QUASAR_FIELDS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_823_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.THE_QUASAR_FIELDS_ESCAPE_THE_KUDZU,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_823_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_QUASAR_FIELDS_MIN_MAXING,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_823_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.THE_QUASAR_FIELDS_KILL_THE_ROCK,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_823_003,
        lambda world: True_(),
    ),
)

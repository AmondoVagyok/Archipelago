"""Every location in High Stakes Room, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import SACCases, SACMissionLocations, SACPlanets, SACSkillPointLocations
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.CASINO
_CASE = SACCases.HIGH_STAKES_ROOM

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.HIGH_STAKES_ROOM_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_814_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.HIGH_STAKES_ROOM_HIGH_RISK_VS_HIGH_STAKES,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_814_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.HIGH_STAKES_ROOM_LUCKY_SEVENS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_814_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.HIGH_STAKES_ROOM_GADGEBOT_STANDS_ALONE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_814_003,
        lambda world: True_(),
    ),
)

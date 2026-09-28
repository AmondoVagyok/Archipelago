"""Every location in Boltaire Gem Wing, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.BOLTAIRE_MUSEUM
_CASE = SACCases.BOLTAIRE_GEM_WING

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACMissionLocations.BOLTAIRE_GEM_WING_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_801_000,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.BOLTAIRE_GEM_WING_THE_NIGHT_FOX,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_801_001,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.BOLTAIRE_GEM_WING_PYRRHIC_VICTORY,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_801_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.BOLTAIRE_GEM_WING_TRIPLE_PLATINUM,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_801_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.BOLTAIRE_GEM_WING_COMPLETE_CASE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_801_002,
        lambda world: True_(),
    ),
)

"""Every location in Underwater Bunker, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.HYDRANO
_CASE = SACCases.UNDERWATER_BUNKER

_BASE = HasAll(SACClankGadgets.JETBOOTS, SACClankGadgets.OMNIKEY, SACClankWeapons.THROWTIE)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACTitaniumBoltLocations.UNDERWATER_BUNKER_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_828_901,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.UNDERWATER_BUNKER_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_828_000,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.UNDERWATER_BUNKER_CLANK_UNDER_GLASS,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_828_001,
        lambda world: _BASE,
    ),
    SACLocation(
        SACSkillPointLocations.UNDERWATER_BUNKER_LEET_HAXXOR,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_828_002,
        lambda world: _BASE,
    ),
    SACLocation(
        SACSkillPointLocations.UNDERWATER_BUNKER_RUST_PROOF,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_828_003,
        lambda world: _BASE,
    ),
    SACLocation(
        SACSkillPointLocations.UNDERWATER_BUNKER_IM_NOT_THERE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_828_004,
        lambda world: _BASE & Has(SACClankGadgets.BLACK_OUT_PEN),
    ),
    SACLocation(
        SACAlienCodeLocations.UNDERWATER_BUNKER_VESSUPS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_828_005,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.UNDERWATER_BUNKER_ADAMS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_828_006,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.UNDERWATER_BUNKER_JEFFS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_828_007,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)

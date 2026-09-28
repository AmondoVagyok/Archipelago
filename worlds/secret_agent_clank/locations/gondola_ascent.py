"""Every location in Gondola Ascent, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.GLACIARA
_CASE = SACCases.GONDOLA_ASCENT

_BASE = HasAll(SACClankGadgets.JETBOOTS, SACClankWeapons.TANGLEVINE)
_OMNIKEY = Has(SACClankGadgets.OMNIKEY) & _BASE

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACTitaniumBoltLocations.GONDOLA_ASCENT_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_810_901,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.GONDOLA_ASCENT_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_810_000,
        lambda world: _BASE,
    ),
    SACLocation(
        SACMissionLocations.GONDOLA_ASCENT_GET_A_LIFT,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_810_001,
        lambda world: _BASE,
    ),
    SACLocation(
        SACSkillPointLocations.GONDOLA_ASCENT_STEEL_RAIN,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_810_003,
        lambda world: _BASE & Has(SACClankWeapons.HOLOKNUCKLES),
    ),
    SACLocation(
        SACCutsceneLocations.GONDOLA_ASCENT_FINISH_GONDOLA_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_810_002,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACAlienCodeLocations.GONDOLA_ASCENT_LEVITICUS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_810_004,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.GONDOLA_ASCENT_CARLS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_810_005,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.GONDOLA_ASCENT_JESS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_810_006,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)

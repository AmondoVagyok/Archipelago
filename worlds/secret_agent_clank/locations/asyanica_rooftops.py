"""Every location in Asyanica Rooftops, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACKeycardLocations,
    SACMissionLocations,
    SACPickups,
    SACPlanets,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.ASYANICA
_CASE = SACCases.ASYANICA_ROOFTOPS

_BASE_RULE = HasAll(SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS)
_OMNIKEY = _BASE_RULE & Has(SACClankGadgets.OMNIKEY)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACPickups.ASYANICA_ROOFTOPS_MINE_LAUNCHER,
        _PLANET,
        _CASE,
        SACLocationType.RATCHET_WEAPON,
        77_803_000,
        lambda world: _BASE_RULE,
    ),
    SACLocation(
        SACPickups.ASYANICA_ROOFTOPS_CUFFLINK_BOMB,
        _PLANET,
        _CASE,
        SACLocationType.CLANK_WEAPON,
        77_803_001,
        lambda world: _BASE_RULE,
    ),
    SACLocation(
        SACPickups.ASYANICA_ROOFTOPS_OMNI_KEY,
        _PLANET,
        _CASE,
        SACLocationType.CLANK_GADGET,
        77_803_002,
        lambda world: _BASE_RULE,
    ),

    SACLocation(
        SACTitaniumBoltLocations.ASYANICA_ROOFTOPS_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_806_901,
        lambda world: _BASE_RULE,
    ),
    SACLocation(
        SACMissionLocations.ASYANICA_ROOFTOPS_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_806_000,
        lambda world: _BASE_RULE,
    ),
    SACLocation(
        SACMissionLocations.ASYANICA_ROOFTOPS_NUMBER_WOO_WORKS_FOR,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_806_001,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACSkillPointLocations.ASYANICA_ROOFTOPS_ROBOT_FINDS_NINJA,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_806_003,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACSkillPointLocations.ASYANICA_ROOFTOPS_BLACK_TIE_AFFAIR,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_806_004,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACSkillPointLocations.ASYANICA_ROOFTOPS_LIKE_THE_WIND,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_806_005,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACKeycardLocations.RED_KEYCARD,
        _PLANET,
        _CASE,
        SACLocationType.KEYCARD,
        77_806_006,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_JHAIROS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_806_007,
        lambda world: Has(SACClankGadgets.THERM_OPTIC_SHADES) & _OMNIKEY,
    ),
    SACLocation(
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_GILBERTS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_806_008,
        lambda world: Has(SACClankGadgets.THERM_OPTIC_SHADES) & _OMNIKEY,
    ),
    SACLocation(
        SACAlienCodeLocations.ASYANICA_ROOFTOPS_RICARDOS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_806_009,
        lambda world: Has(SACClankGadgets.THERM_OPTIC_SHADES) & _OMNIKEY,
    ),
)

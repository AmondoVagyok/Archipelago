"""Every location in Galactic Bolt Reserve, each carrying its planet, case and access rule."""
from rule_builder.rules import Has, HasAll, True_

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

_PLANET = SACPlanets.VENANTONIO
_CASE = SACCases.GALACTIC_BOLT_RESERVE

_BASE = HasAll(SACClankWeapons.CUFFLINK, SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS)
_OMNIKEY = _BASE & Has(SACClankGadgets.OMNIKEY)
_HOLOMONICLE = _OMNIKEY & Has(SACClankGadgets.HOLOMONOCLE)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_818_901,
        lambda world: _BASE,
    ),
    SACLocation(
        SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_2,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_818_902,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_3,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_818_903,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACMissionLocations.GALACTIC_BOLT_RESERVE_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_818_000,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACMissionLocations.GALACTIC_BOLT_RESERVE_HARD_CURRENCY,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_818_001,
        lambda world: _OMNIKEY,
    ),
    SACLocation(
        SACMissionLocations.GALACTIC_BOLT_RESERVE_THE_BIG_HEIST,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_818_002,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACSkillPointLocations.GALACTIC_BOLT_RESERVE_WITH_INTEREST,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_818_005,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACSkillPointLocations.GALACTIC_BOLT_RESERVE_ANDROIDS_IN_DISGUISE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_818_006,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACSkillPointLocations.GALACTIC_BOLT_RESERVE_VAULT_VAULT,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_818_007,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACCutsceneLocations.GALACTIC_BOLT_RESERVE_ENTER_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_818_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.GALACTIC_BOLT_RESERVE_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_818_004,
        lambda world: _HOLOMONICLE,
    ),
    SACLocation(
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_AVERYS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_818_008,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_LESLEYS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_818_009,
        lambda world: _OMNIKEY & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_DAVES_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_818_010,
        lambda world: _HOLOMONICLE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)

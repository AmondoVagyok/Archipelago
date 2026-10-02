"""Every location in Spaceship Graveyard, each carrying its planet, case and access rule."""
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
from ..rules.rule_helpers import HasProjectileWeapon
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.SPACESHIP_GRAVEYARD
_CASE = SACCases.SPACESHIP_GRAVEYARD

_BASE = Has(SACClankGadgets.JETBOOTS) & HasProjectileWeapon()
_OMNIKEY = _BASE & Has(SACClankGadgets.OMNIKEY)
_TANGLE = _OMNIKEY & Has(SACClankWeapons.TANGLEVINE)

LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(
        SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_1,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_821_901,
        lambda world: _BASE,
    ),
    SACLocation(
        SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_2,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_821_902,
        lambda world: _BASE & HasAll(SACClankWeapons.THROWTIE, SACClankGadgets.OMNIKEY),
    ),
    SACLocation(
        SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_3,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_821_903,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_4,
        _PLANET,
        _CASE,
        SACLocationType.TITANIUM_BOLT,
        77_821_904,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACMissionLocations.SPACESHIP_GRAVEYARD_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_821_000,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACMissionLocations.SPACESHIP_GRAVEYARD_TRACKING_THE_KINGPIN,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_821_001,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACSkillPointLocations.SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_821_004,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACSkillPointLocations.SPACESHIP_GRAVEYARD_REVENANT,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_821_005,
        lambda world: _TANGLE & Has(SACClankGadgets.HOLOMONOCLE),
    ),
    SACLocation(
        SACCutsceneLocations.SPACESHIP_GRAVEYARD_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_821_003,
        lambda world: _TANGLE,
    ),
    SACLocation(
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_MATTS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_821_006,
        lambda world: _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_KENS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_821_007,
        lambda world: _TANGLE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
    SACLocation(
        SACAlienCodeLocations.SPACESHIP_GRAVEYARD_JAREDS_SECRET,
        _PLANET,
        _CASE,
        SACLocationType.ALIEN_CODE,
        77_821_008,
        lambda world: _TANGLE & Has(SACClankGadgets.THERM_OPTIC_SHADES),
    ),
)

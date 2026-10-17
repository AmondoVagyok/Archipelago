from rule_builder.rules import Has, HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACCutsceneLocations,
    SACMissionLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
    SACVendor,
)
from ..rules import HasProjectileWeapon, VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_TANGLE_ITEMS = (SACClankGadgets.JETBOOTS, SACClankGadgets.OMNIKEY, SACClankWeapons.TANGLEVINE)
_BASE = Has(SACClankGadgets.JETBOOTS) & HasProjectileWeapon()
_TANGLE = HasAll(*_TANGLE_ITEMS) & HasProjectileWeapon()

_VENDOR = VendorCaseRule(SACCases.SPACESHIP_GRAVEYARD)

REGION = CaseRegion(SACCases.SPACESHIP_GRAVEYARD, (
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_1, SACLocationType.TITANIUM_BOLT, _BASE, flag_bit=0),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_2,
                SACLocationType.TITANIUM_BOLT, HasAll(SACClankGadgets.JETBOOTS, SACClankWeapons.THROWTIE, SACClankGadgets.OMNIKEY) & HasProjectileWeapon(),
                flag_bit=2),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_3, SACLocationType.TITANIUM_BOLT, _TANGLE, flag_bit=1),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_4, SACLocationType.TITANIUM_BOLT, _TANGLE, flag_bit=3),
    SACLocation(SACMissionLocations.SPACESHIP_GRAVEYARD_COMPLETE, SACLocationType.CASE_COMPLETE, _TANGLE),
    SACLocation(SACMissionLocations.SPACESHIP_GRAVEYARD_TRACKING_THE_KINGPIN, SACLocationType.MISSION, _TANGLE),
    SACLocation(SACSkillPointLocations.SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE, SACLocationType.SKILL_POINT, _TANGLE),
    SACLocation(SACSkillPointLocations.SPACESHIP_GRAVEYARD_REVENANT,
                SACLocationType.SKILL_POINT, HasAll(*_TANGLE_ITEMS, SACClankGadgets.HOLOMONOCLE) & HasProjectileWeapon()),
    SACLocation(SACCutsceneLocations.SPACESHIP_GRAVEYARD_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE, _TANGLE),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_MATTS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(SACClankGadgets.JETBOOTS, SACClankGadgets.THERM_OPTIC_SHADES) & HasProjectileWeapon(),
                flag_bit=0),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_KENS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_TANGLE_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES) & HasProjectileWeapon(),
                flag_bit=1),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_JAREDS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_TANGLE_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES) & HasProjectileWeapon(),
                flag_bit=2),
    SACLocation(SACVendor.SPACESHIP_GRAVEYARD_SHOCK_ROCKET_PORK_BOMB_GUN_TASTY_PIGS,
                SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.SPACESHIP_GRAVEYARD_SHOCK_ROCKET_STATIC_CHARGE, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.SPACESHIP_GRAVEYARD_SHOCK_PLASMA_WHIP_FIRE_SNAKE, SACLocationType.MOD_VENDOR, _VENDOR),
))

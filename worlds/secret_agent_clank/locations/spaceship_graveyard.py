"""Spaceship Graveyard: the case region and every location in it, with its access rule."""
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
)
from ..rules.rule_helpers import HasProjectileWeapon
from .model import CaseRegion, SACLocation, SACLocationType

_BASE = Has(SACClankGadgets.JETBOOTS) & HasProjectileWeapon()
_OMNIKEY = _BASE & Has(SACClankGadgets.OMNIKEY)
_TANGLE = _OMNIKEY & Has(SACClankWeapons.TANGLEVINE)

REGION = CaseRegion(SACCases.SPACESHIP_GRAVEYARD, (
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_1, SACLocationType.TITANIUM_BOLT, _BASE),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_2,
                SACLocationType.TITANIUM_BOLT, _BASE & HasAll(SACClankWeapons.THROWTIE, SACClankGadgets.OMNIKEY)),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_3, SACLocationType.TITANIUM_BOLT, _TANGLE),
    SACLocation(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_4, SACLocationType.TITANIUM_BOLT, _TANGLE),
    SACLocation(SACMissionLocations.SPACESHIP_GRAVEYARD_COMPLETE, SACLocationType.CASE_COMPLETE, _TANGLE),
    SACLocation(SACMissionLocations.SPACESHIP_GRAVEYARD_TRACKING_THE_KINGPIN, SACLocationType.MISSION, _TANGLE),
    SACLocation(SACSkillPointLocations.SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE, SACLocationType.SKILL_POINT, _TANGLE),
    SACLocation(SACSkillPointLocations.SPACESHIP_GRAVEYARD_REVENANT,
                SACLocationType.SKILL_POINT, _TANGLE & Has(SACClankGadgets.HOLOMONOCLE)),
    SACLocation(SACCutsceneLocations.SPACESHIP_GRAVEYARD_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE, _TANGLE),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_MATTS_SECRET,
                SACLocationType.ALIEN_CODE, _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_KENS_SECRET,
                SACLocationType.ALIEN_CODE, _TANGLE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_JAREDS_SECRET,
                SACLocationType.ALIEN_CODE, _TANGLE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
))

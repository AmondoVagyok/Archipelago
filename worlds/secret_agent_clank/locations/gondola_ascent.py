"""Gondola Ascent: the case region and every location in it, with its access rule."""
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
from .model import CaseRegion, SACLocation, SACLocationType

_BASE = HasAll(SACClankGadgets.JETBOOTS, SACClankWeapons.TANGLEVINE)
_OMNIKEY = Has(SACClankGadgets.OMNIKEY) & _BASE

REGION = CaseRegion(SACCases.GONDOLA_ASCENT, (
    SACLocation(SACTitaniumBoltLocations.GONDOLA_ASCENT_1, SACLocationType.TITANIUM_BOLT, _BASE),
    SACLocation(SACMissionLocations.GONDOLA_ASCENT_COMPLETE, SACLocationType.CASE_COMPLETE, _BASE),
    SACLocation(SACMissionLocations.GONDOLA_ASCENT_GET_A_LIFT, SACLocationType.MISSION, _BASE),
    SACLocation(SACSkillPointLocations.GONDOLA_ASCENT_STEEL_RAIN,
                SACLocationType.SKILL_POINT, _BASE & Has(SACClankWeapons.HOLOKNUCKLES)),
    SACLocation(SACCutsceneLocations.GONDOLA_ASCENT_FINISH_GONDOLA_CUTSCENE, SACLocationType.CUTSCENE, _OMNIKEY),
    SACLocation(SACAlienCodeLocations.GONDOLA_ASCENT_LEVITICUS_SECRET,
                SACLocationType.ALIEN_CODE, _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.GONDOLA_ASCENT_CARLS_SECRET,
                SACLocationType.ALIEN_CODE, _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.GONDOLA_ASCENT_JESS_SECRET,
                SACLocationType.ALIEN_CODE, _BASE & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
))

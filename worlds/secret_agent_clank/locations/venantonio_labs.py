"""Venantonio Labs: the case region and every location in it, with its access rule."""
from rule_builder.rules import Has, HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPickups,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

_BASE = HasAll(SACClankWeapons.CUFFLINK, SACClankGadgets.OMNIKEY)
_BRIEFCASE_PATH = HasAll(SACClankWeapons.FLAMETHROWERPEN, SACClankWeapons.CUFFLINK)
_FINISH = _BRIEFCASE_PATH & HasAll(SACClankGadgets.OMNIKEY, SACClankGadgets.JETBOOTS)

REGION = CaseRegion(SACCases.VENANTONIO_LABS, (
    SACLocation(SACPickups.VENANTONIO_LABS_BLOWTORCH_BRIEFCASE, SACLocationType.CLANK_WEAPON, _BASE),
    SACLocation(SACTitaniumBoltLocations.VENANTONIO_LABS_1, SACLocationType.TITANIUM_BOLT, _BASE),
    SACLocation(SACTitaniumBoltLocations.VENANTONIO_LABS_2, SACLocationType.TITANIUM_BOLT, _BRIEFCASE_PATH),
    SACLocation(SACMissionLocations.VENANTONIO_LABS_COMPLETE, SACLocationType.CASE_COMPLETE, _FINISH),
    SACLocation(SACMissionLocations.VENANTONIO_LABS_CRASHING_THE_PARTY, SACLocationType.MISSION, _BASE),
    SACLocation(SACMissionLocations.VENANTONIO_LABS_OUT_OF_THE_FRYING_PAN, SACLocationType.MISSION, _FINISH),
    SACLocation(SACSkillPointLocations.VENANTONIO_LABS_ALL_SLIME_MUST_BURN,
                SACLocationType.SKILL_POINT, _BASE & Has(SACClankWeapons.FLAMETHROWERPEN)),
    SACLocation(SACSkillPointLocations.VENANTONIO_LABS_RAMMING_SPEED, SACLocationType.SKILL_POINT, _BRIEFCASE_PATH),
    SACLocation(SACCutsceneLocations.VENANTONIO_LABS_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.VENANTONIO_LABS_OPEN_GREEN_DOOR_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.VENANTONIO_LABS_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE, _FINISH),
    SACLocation(SACAlienCodeLocations.VENANTONIO_LABS_GERARDS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.VENANTONIO_LABS_ALEXS_SECRET,
                SACLocationType.ALIEN_CODE, _BRIEFCASE_PATH & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.VENANTONIO_LABS_HAROONS_SECRET,
                SACLocationType.ALIEN_CODE, _BRIEFCASE_PATH & Has(SACClankGadgets.THERM_OPTIC_SHADES)),
))

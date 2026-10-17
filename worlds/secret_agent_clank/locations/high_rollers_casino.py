from rule_builder.rules import Has, HasAll, True_

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
    SACVendor,
)
from ..rules import ProgressiveChallengeModeRule, VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_BASE = Has(SACClankGadgets.HOLOMONOCLE)
_complete = HasAll(SACClankGadgets.HOLOMONOCLE, SACClankWeapons.CUFFLINK)

_VENDOR = VendorCaseRule(SACCases.HIGH_ROLLERS_CASINO)
_CHALLENGE_VENDOR = _VENDOR & ProgressiveChallengeModeRule()

REGION = CaseRegion(SACCases.HIGH_ROLLERS_CASINO, (
    SACLocation(SACPickups.HIGH_ROLLERS_CASINO_HOLO_MONOCLE, SACLocationType.CLANK_GADGET),
    SACLocation(SACTitaniumBoltLocations.HIGH_ROLLERS_CASINO_1,
                SACLocationType.TITANIUM_BOLT, HasAll(SACClankGadgets.HOLOMONOCLE, SACClankGadgets.OMNIKEY),
                flag_bit=0),
    SACLocation(SACMissionLocations.HIGH_ROLLERS_CASINO_COMPLETE, SACLocationType.CASE_COMPLETE, _complete),
    SACLocation(SACMissionLocations.HIGH_ROLLERS_CASINO_EXPLORE_PARADISE, SACLocationType.MISSION, _BASE),
    SACLocation(SACMissionLocations.HIGH_ROLLERS_CASINO_PARADISE_EXPLOITED, SACLocationType.MISSION, _BASE),
    SACLocation(SACSkillPointLocations.HIGH_ROLLERS_CASINO_BEAT_THE_HOUSE, SACLocationType.SKILL_POINT, _BASE),
    SACLocation(SACCutsceneLocations.HIGH_ROLLERS_CASINO_ENTER_CUTSCENE, SACLocationType.CUTSCENE, True_()),
    SACLocation(SACCutsceneLocations.HIGH_ROLLERS_CASINO_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE, _complete),
    SACLocation(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_COLINS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=0),
    SACLocation(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_SHANES_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(SACClankGadgets.HOLOMONOCLE, SACClankGadgets.THERM_OPTIC_SHADES),
                flag_bit=1),
    SACLocation(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_THE_PING_PONG_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(SACClankGadgets.HOLOMONOCLE, SACClankGadgets.THERM_OPTIC_SHADES),
                flag_bit=2),
    SACLocation(SACVendor.HIGH_ROLLERS_CASINO_HYPNO_WATCH, SACLocationType.VENDOR, _VENDOR),
    SACLocation(SACVendor.HIGH_ROLLERS_CASINO_PORK_BOBM_GUN, SACLocationType.VENDOR, _VENDOR),
    SACLocation(SACVendor.HIGH_ROLLERS_CASINO_BEE_MINE_MK_II_KILLER_HONEY, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.HIGH_ROLLERS_CASINO_TITAN_MEAT_MORTAR, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
))

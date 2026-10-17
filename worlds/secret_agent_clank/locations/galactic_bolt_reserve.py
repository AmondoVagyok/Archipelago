from rule_builder.rules import HasAll

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
from ..rules import ProgressiveChallengeModeRule, VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_BASE_ITEMS = (SACClankWeapons.CUFFLINK, SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS)
_OMNIKEY_ITEMS = (*_BASE_ITEMS, SACClankGadgets.OMNIKEY)
_HOLOMONICLE_ITEMS = (*_OMNIKEY_ITEMS, SACClankGadgets.HOLOMONOCLE)
_BASE = HasAll(*_BASE_ITEMS)
_OMNIKEY = HasAll(*_OMNIKEY_ITEMS)
_HOLOMONICLE = HasAll(*_HOLOMONICLE_ITEMS)

_VENDOR = VendorCaseRule(SACCases.GALACTIC_BOLT_RESERVE)
_CHALLENGE_VENDOR = _VENDOR & ProgressiveChallengeModeRule()

REGION = CaseRegion(SACCases.GALACTIC_BOLT_RESERVE, (
    SACLocation(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_1, SACLocationType.TITANIUM_BOLT, _BASE, flag_bit=0),
    SACLocation(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_2, SACLocationType.TITANIUM_BOLT, _OMNIKEY, flag_bit=1),
    SACLocation(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_3, SACLocationType.TITANIUM_BOLT, _HOLOMONICLE,
                flag_bit=2),
    SACLocation(SACMissionLocations.GALACTIC_BOLT_RESERVE_COMPLETE, SACLocationType.CASE_COMPLETE, _HOLOMONICLE),
    SACLocation(SACMissionLocations.GALACTIC_BOLT_RESERVE_HARD_CURRENCY, SACLocationType.MISSION, _OMNIKEY),
    SACLocation(SACMissionLocations.GALACTIC_BOLT_RESERVE_THE_BIG_HEIST, SACLocationType.MISSION, _HOLOMONICLE),
    SACLocation(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_WITH_INTEREST, SACLocationType.SKILL_POINT, _HOLOMONICLE),
    SACLocation(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_ANDROIDS_IN_DISGUISE,
                SACLocationType.SKILL_POINT, _HOLOMONICLE),
    SACLocation(SACCutsceneLocations.GALACTIC_BOLT_RESERVE_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.GALACTIC_BOLT_RESERVE_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE, _HOLOMONICLE),
    SACLocation(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_AVERYS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_BASE_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=1),
    SACLocation(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_LESLEYS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_OMNIKEY_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=0),
    SACLocation(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_DAVES_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_HOLOMONICLE_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES),
                flag_bit=2),
    SACLocation(SACVendor.GALACTIC_BOLT_RESERVE_SHOCK_ROCKET, SACLocationType.VENDOR, _VENDOR),
    SACLocation(SACVendor.GALACTIC_BOLT_RESERVE_BOLT_GRABBER, SACLocationType.VENDOR, _VENDOR),
    SACLocation(SACVendor.GALACTIC_BOLT_RESERVE_TITAN_ELECTRO_ROCKET, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
))

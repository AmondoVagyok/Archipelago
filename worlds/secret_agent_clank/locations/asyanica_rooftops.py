from rule_builder.rules import HasAll

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACClankWeapons,
    SACKeycardLocations,
    SACMissionLocations,
    SACPickups,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
    SACVendor,
)
from ..rules import ProgressiveChallengeModeRule, VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_BASE_ITEMS = (SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS)
_OMNIKEY_ITEMS = (*_BASE_ITEMS, SACClankGadgets.OMNIKEY)
_BASE_RULE = HasAll(*_BASE_ITEMS)
_OMNIKEY = HasAll(*_OMNIKEY_ITEMS)

_VENDOR = VendorCaseRule(SACCases.ASYANICA_ROOFTOPS)
_CHALLENGE_VENDOR = _VENDOR & ProgressiveChallengeModeRule()

REGION = CaseRegion(SACCases.ASYANICA_ROOFTOPS, (
    SACLocation(SACPickups.ASYANICA_ROOFTOPS_MINE_LAUNCHER, SACLocationType.RATCHET_WEAPON, _OMNIKEY),
    SACLocation(SACPickups.ASYANICA_ROOFTOPS_CUFFLINK_BOMB, SACLocationType.CLANK_WEAPON, _OMNIKEY),
    SACLocation(SACPickups.ASYANICA_ROOFTOPS_OMNI_KEY, SACLocationType.CLANK_GADGET, _BASE_RULE),
    SACLocation(SACTitaniumBoltLocations.ASYANICA_ROOFTOPS_1, SACLocationType.TITANIUM_BOLT, _BASE_RULE, flag_bit=0),
    SACLocation(SACMissionLocations.ASYANICA_ROOFTOPS_COMPLETE, SACLocationType.CASE_COMPLETE, _BASE_RULE),
    SACLocation(SACMissionLocations.ASYANICA_ROOFTOPS_NUMBER_WOO_WORKS_FOR, SACLocationType.MISSION, _OMNIKEY),
    SACLocation(SACSkillPointLocations.ASYANICA_ROOFTOPS_ROBOT_FINDS_NINJA, SACLocationType.SKILL_POINT, _OMNIKEY),
    SACLocation(SACSkillPointLocations.ASYANICA_ROOFTOPS_BLACK_TIE_AFFAIR, SACLocationType.SKILL_POINT, _OMNIKEY),
    SACLocation(SACSkillPointLocations.ASYANICA_ROOFTOPS_LIKE_THE_WIND, SACLocationType.SKILL_POINT, _OMNIKEY),
    SACLocation(SACKeycardLocations.RED_KEYCARD, SACLocationType.KEYCARD, _OMNIKEY),
    SACLocation(SACAlienCodeLocations.ASYANICA_ROOFTOPS_JHAIROS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_BASE_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=0),
    SACLocation(SACAlienCodeLocations.ASYANICA_ROOFTOPS_GILBERTS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_OMNIKEY_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=1),
    SACLocation(SACAlienCodeLocations.ASYANICA_ROOFTOPS_RICARDOS_SECRET,
                SACLocationType.ALIEN_CODE, HasAll(*_OMNIKEY_ITEMS, SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=2),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_DUAL_LACERATOR_SEEKER, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_DUAL_LACERATOR_HUNTER, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_DUAL_SHARD_GUN_ICE_HALO, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_WALLOPER_LIGHTNING_SPEED, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_PROTO_WRIST_MORTAR, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
    SACLocation(SACVendor.ASYANICA_ROOFTOPS_TITAN_ORDNANCE_LAUNCHER, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
))

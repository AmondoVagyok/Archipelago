from rule_builder.rules import Has

from ..constants import (
    SACAlienCodeLocations,
    SACCases,
    SACClankGadgets,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPickups,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
    SACVendor,
)
from ..rules import ProgressiveChallengeModeRule, VendorCaseRule
from .model import CaseRegion, SACLocation, SACLocationType

_VENDOR = VendorCaseRule(SACCases.AZCOTAL_ALLEY)
_CHALLENGE_VENDOR = _VENDOR & ProgressiveChallengeModeRule()

REGION = CaseRegion(SACCases.AZCOTAL_ALLEY, (
    SACLocation(SACPickups.AZCOTAL_ALLEY_BEE_MINE_MK_II, SACLocationType.RATCHET_WEAPON),
    SACLocation(SACPickups.AZCOTAL_ALLEY_TANGLEVINE_CARNATION, SACLocationType.CLANK_WEAPON),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_1, SACLocationType.TITANIUM_BOLT, flag_bit=0),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_2, SACLocationType.TITANIUM_BOLT, flag_bit=1),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_3, SACLocationType.TITANIUM_BOLT, flag_bit=2),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_THE_KINGPIN, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_ALL_THE_KINGPIN_S_MEN, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_MASTER_OF_DISGUISE, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_TRASH_TALK, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_DEADLY_HANDS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.AZCOTAL_ALLEY_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.AZCOTAL_ALLEY_MEET_JACK_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_JONS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=1),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_THE_3_JASONS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=2),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_TRAVIS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES), flag_bit=0),
    SACLocation(SACVendor.AZCOTAL_ALLEY_AGENCY_PDA, SACLocationType.VENDOR, _VENDOR),
    SACLocation(SACVendor.AZCOTAL_ALLEY_BEE_MINE_MK_II_EXPLOSIVE_NATURE, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.AZCOTAL_ALLEY_MINE_LAUNCHER_ORDNANCE, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.AZCOTAL_ALLEY_MINE_LAUNCHER_PERSISTENCE, SACLocationType.MOD_VENDOR, _VENDOR),
    SACLocation(SACVendor.AZCOTAL_ALLEY_PROTO_KUDZU_TANGLE, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
    SACLocation(SACVendor.AZCOTAL_ALLEY_TITAN_KILLER_BEE_MINE, SACLocationType.TITAN_VENDOR, _CHALLENGE_VENDOR),
))

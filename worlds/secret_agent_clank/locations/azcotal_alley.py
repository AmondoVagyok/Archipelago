"""Azcotal Alley: the case region and every location in it, with its access rule."""
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
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.AZCOTAL_ALLEY, (
    SACLocation(SACPickups.AZCOTAL_ALLEY_BEE_MINE_MK_II, SACLocationType.RATCHET_WEAPON),
    SACLocation(SACPickups.AZCOTAL_ALLEY_TANGLEVINE_CARNATION, SACLocationType.CLANK_WEAPON),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_1, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_2, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACTitaniumBoltLocations.AZCOTAL_ALLEY_3, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_THE_KINGPIN, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.AZCOTAL_ALLEY_ALL_THE_KINGPIN_S_MEN, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_MASTER_OF_DISGUISE, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_TRASH_TALK, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.AZCOTAL_ALLEY_DEADLY_HANDS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.AZCOTAL_ALLEY_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.AZCOTAL_ALLEY_MEET_JACK_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_JONS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_THE_3_JASONS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES)),
    SACLocation(SACAlienCodeLocations.AZCOTAL_ALLEY_TRAVIS_SECRET,
                SACLocationType.ALIEN_CODE, Has(SACClankGadgets.THERM_OPTIC_SHADES)),
))

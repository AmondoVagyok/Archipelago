"""Inside the A-Eye: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACGadgetbotChallengeLocations,
    SACKeycardLocations,
    SACMissionLocations,
    SACSkillPointLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.INSIDE_THE_A_EYE, (
    # Preserve the AP name/ID and native flag; earned in Vaultbreakers.
    SACLocation(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_VAULT_VAULT, SACLocationType.SKILL_POINT),
    SACLocation(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_VAULTBREAKERS, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_DARK_HELMET, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_GO_LONG, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACMissionLocations.INSIDE_THE_A_EYE_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.INSIDE_THE_A_EYE_PAYBACK_S_A_PUNCH, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.INSIDE_THE_A_EYE_MYE_MYNDE_IS_GOING, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.INSIDE_THE_A_EYE_DIA_DE_LOS_MUERTOS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.INSIDE_THE_A_EYE_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACKeycardLocations.BLUE_KEYCARD, SACLocationType.KEYCARD),
))

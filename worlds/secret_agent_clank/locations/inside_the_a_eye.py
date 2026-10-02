"""Every location in Inside the A-Eye, each carrying its planet, case and access rule."""
from rule_builder.rules import True_

from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACGadgetbotChallengeLocations,
    SACKeycardLocations,
    SACMissionLocations,
    SACPlanets,
    SACSkillPointLocations,
)
from .model import SACLocation, SACLocationType

_PLANET = SACPlanets.FORT_SPROCKET
_CASE = SACCases.INSIDE_THE_A_EYE

LOCATIONS: tuple[SACLocation, ...] = (
    # Preserve the AP name/ID and native flag; earned in Vaultbreakers.
    SACLocation(
        SACSkillPointLocations.GALACTIC_BOLT_RESERVE_VAULT_VAULT,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_818_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_VAULTBREAKERS,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_819_002,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_DARK_HELMET,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_819_003,
        lambda world: True_(),
    ),
    SACLocation(
        SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_GO_LONG,
        _PLANET,
        _CASE,
        SACLocationType.GADGETBOT_CHALLENGE,
        77_819_004,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.INSIDE_THE_A_EYE_COMPLETE,
        _PLANET,
        _CASE,
        SACLocationType.CASE_COMPLETE,
        77_819_005,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.INSIDE_THE_A_EYE_PAYBACK_S_A_PUNCH,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_819_006,
        lambda world: True_(),
    ),
    SACLocation(
        SACMissionLocations.INSIDE_THE_A_EYE_MYE_MYNDE_IS_GOING,
        _PLANET,
        _CASE,
        SACLocationType.MISSION,
        77_819_007,
        lambda world: True_(),
    ),
    SACLocation(
        SACSkillPointLocations.INSIDE_THE_A_EYE_DIA_DE_LOS_MUERTOS,
        _PLANET,
        _CASE,
        SACLocationType.SKILL_POINT,
        77_819_009,
        lambda world: True_(),
    ),
    SACLocation(
        SACCutsceneLocations.INSIDE_THE_A_EYE_COMPLETE_CUTSCENE,
        _PLANET,
        _CASE,
        SACLocationType.CUTSCENE,
        77_819_008,
        lambda world: True_(),
    ),
    SACLocation(
        SACKeycardLocations.BLUE_KEYCARD,
        _PLANET,
        _CASE,
        SACLocationType.KEYCARD,
        77_819_010,
    ),
)

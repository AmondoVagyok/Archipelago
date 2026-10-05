"""Rooftop Deathtrap: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACGadgetbotChallengeLocations,
    SACMissionLocations,
    SACSkillPointLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.ROOFTOP_DEATHTRAP, (
    SACLocation(SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_RESCUE_CLANK, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_WORKING_DOWN, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_GREAT_DIVIDE, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACMissionLocations.ROOFTOP_DEATHTRAP_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.ROOFTOP_DEATHTRAP_GET_A_CLUE, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.ROOFTOP_DEATHTRAP_FREE_AGENT_CLANK, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.ROOFTOP_DEATHTRAP_THE_HALLS_OF_ASYANICA, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.ROOFTOP_DEATHTRAP_SPEED_DEMON, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.ROOFTOP_DEATHTRAP_PERFECT_CHROME_FINISH, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.ROOFTOP_DEATHTRAP_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.ROOFTOP_DEATHTRAP_RESCURE_CLANK_CUTSCENE, SACLocationType.CUTSCENE),
))

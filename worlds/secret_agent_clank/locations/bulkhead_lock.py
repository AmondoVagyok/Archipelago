"""Bulkhead Lock: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACGadgetbotChallengeLocations,
    SACMissionLocations,
    SACSkillPointLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.BULKHEAD_LOCK, (
    SACLocation(SACGadgetbotChallengeLocations.BULKHEAD_LOCK_KNOCKIN_ON_KLUNKS_DOOR,
                SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACGadgetbotChallengeLocations.BULKHEAD_LOCK_MISSION_POSSIBLE, SACLocationType.GADGETBOT_CHALLENGE),
    SACLocation(SACMissionLocations.BULKHEAD_LOCK_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.BULKHEAD_LOCK_UNDERWATER_BASE, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.BULKHEAD_LOCK_LOCKED_DOOR, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.BULKHEAD_LOCK_INSULT_TO_INJURY, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.BULKHEAD_LOCK_CEREAL_DECODER_RING, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.BULKHEAD_LOCK_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

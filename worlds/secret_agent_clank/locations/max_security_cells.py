"""Max-Security Cells: the case region and every location in it, with its access rule."""
from ..constants import (
    SACCases,
    SACCutsceneLocations,
    SACMissionLocations,
    SACPickups,
    SACRatchetChallengeLocations,
    SACSkillPointLocations,
    SACTitaniumBoltLocations,
)
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.MAX_SECURITY_CELLS, (
    SACLocation(SACPickups.MAX_SECURITY_CELLS_SHARDGUN, SACLocationType.RATCHET_WEAPON),
    SACLocation(SACPickups.MAX_SECURITY_CELLS_WALLOPER, SACLocationType.RATCHET_WEAPON),
    SACLocation(SACRatchetChallengeLocations.MAX_SECURITY_CELLS_KARMIC_BREAKDOWN, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.MAX_SECURITY_CELLS_NO_SHELTER, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.MAX_SECURITY_CELLS_PAST_DUE, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.MAX_SECURITY_CELLS_SPEAK_SOFTLY_AND, SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACRatchetChallengeLocations.MAX_SECURITY_CELLS_MEGA_CHALLENGE_CELLBLOCK,
                SACLocationType.RATCHET_CHALLENGE),
    SACLocation(SACTitaniumBoltLocations.MAX_SECURITY_CELLS_1, SACLocationType.TITANIUM_BOLT),
    SACLocation(SACMissionLocations.MAX_SECURITY_CELLS_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.MAX_SECURITY_CELLS_LIFE_IN_PRISON, SACLocationType.MISSION),
    SACLocation(SACMissionLocations.MAX_SECURITY_CELLS_CONSECUTIVE_LIFE_SENTENCES, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.MAX_SECURITY_CELLS_STAINLESS_STEEL, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.MAX_SECURITY_CELLS_PLAYING_WITH_FIRE, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.MAX_SECURITY_CELLS_ENTER_CUTSCENE, SACLocationType.CUTSCENE),
))

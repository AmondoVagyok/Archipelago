"""Klunk's Lair: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.KLUNKS_LAIR, (
    SACLocation(SACMissionLocations.KLUNKS_LAIR_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.KLUNKS_LAIR_ALL_THE_MARBLES, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.KLUNKS_LAIR_TURN_THE_TABLES, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.KLUNKS_LAIR_PRETTY_GOOD_LIKENESS, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.KLUNKS_LAIR_ENTERE_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.KLUNKS_LAIR_MID_FIGHT_CUTSCENE_FOR_ROBO_RATCHET, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.KLUNKS_LAIR_COMPLETE_CUTSCENE, SACLocationType.CUTSCENE),
    SACLocation(SACCutsceneLocations.KLUNKS_LAIR_HIGH_IMPACT_GAMES_CUTSCENE_WITH_GIANT_CLANK, SACLocationType.CUTSCENE),
))

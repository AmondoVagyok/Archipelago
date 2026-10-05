"""Boltaire Gem Wing: the case region and every location in it, with its access rule."""
from ..constants import SACCases, SACCutsceneLocations, SACMissionLocations, SACSkillPointLocations
from .model import CaseRegion, SACLocation, SACLocationType

REGION = CaseRegion(SACCases.BOLTAIRE_GEM_WING, (
    SACLocation(SACMissionLocations.BOLTAIRE_GEM_WING_COMPLETE, SACLocationType.CASE_COMPLETE),
    SACLocation(SACMissionLocations.BOLTAIRE_GEM_WING_THE_NIGHT_FOX, SACLocationType.MISSION),
    SACLocation(SACSkillPointLocations.BOLTAIRE_GEM_WING_PYRRHIC_VICTORY, SACLocationType.SKILL_POINT),
    SACLocation(SACSkillPointLocations.BOLTAIRE_GEM_WING_TRIPLE_PLATINUM, SACLocationType.SKILL_POINT),
    SACLocation(SACCutsceneLocations.BOLTAIRE_GEM_WING_COMPLETE_CASE_CUTSCENE, SACLocationType.CUTSCENE),
))

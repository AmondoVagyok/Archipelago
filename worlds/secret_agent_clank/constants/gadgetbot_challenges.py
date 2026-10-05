"""Gadgetbot Challenge locations and their native completion flags."""
from dataclasses import dataclass

from .types import EventFlag


@dataclass(frozen=True)
class SACGadgetbotChallengeLocations:
    ROOFTOP_DEATHTRAP_RESCUE_CLANK = "Asyanica (Gadgetbots) - Rooftop Deathtrap: Rescue Clank"
    ROOFTOP_DEATHTRAP_WORKING_DOWN = "Asyanica (Gadgetbots) - Rooftop Deathtrap: Working Down"
    ROOFTOP_DEATHTRAP_GREAT_DIVIDE = "Asyanica (Gadgetbots) - Rooftop Deathtrap: Great Divide"
    INSIDE_THE_A_EYE_VAULTBREAKERS = "Fort Sprocket (Gadgetbots) - Inside the A-Eye: Vaultbreakers"
    INSIDE_THE_A_EYE_DARK_HELMET = "Fort Sprocket (Gadgetbots) - Inside the A-Eye: Dark Helmet"
    INSIDE_THE_A_EYE_GO_LONG = "Fort Sprocket (Gadgetbots) - Inside the A-Eye: Go Long"
    BULKHEAD_LOCK_KNOCKIN_ON_KLUNKS_DOOR = "Hydrano (Gadgetbots) - Bulkhead Lock: Knockin' on Klunk's Door"
    BULKHEAD_LOCK_MISSION_POSSIBLE = "Hydrano (Gadgetbots) - Bulkhead Lock: Mission: Possible"


GADGETBOT_CHALLENGE_FLAGS: dict[str, EventFlag] = {
    SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_RESCUE_CLANK: EventFlag(0x206C7A, 0b00000001),
    SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_WORKING_DOWN: EventFlag(0x206C7B, 0b00000001),
    SACGadgetbotChallengeLocations.ROOFTOP_DEATHTRAP_GREAT_DIVIDE: EventFlag(0x206C7C, 0b00000001),
    SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_VAULTBREAKERS: EventFlag(0x206C7F, 0b00000001),
    SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_DARK_HELMET: EventFlag(0x206C80, 0b00000001),
    SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_GO_LONG: EventFlag(0x206C81, 0b00000001),
    SACGadgetbotChallengeLocations.BULKHEAD_LOCK_KNOCKIN_ON_KLUNKS_DOOR: EventFlag(0x206C83, 0b00000001),
    SACGadgetbotChallengeLocations.BULKHEAD_LOCK_MISSION_POSSIBLE: EventFlag(0x206C84, 0b00000001),
}

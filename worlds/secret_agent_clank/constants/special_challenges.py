"""Special Missions challenge locations. Each address is a plain 0/1 byte, confirmed live."""
from dataclasses import dataclass

from .types import EventFlag


@dataclass(frozen=True)
class SACSpecialChallengeLocations:
    VENANTONIO_CANALS_VEHICLE_GREAT_ESCAPE = "Venantonio (Special Missions) - Venantonio Canals: Great Escape"
    VENANTONIO_CANALS_VEHICLE_SPEEDBOATING = "Venantonio (Special Missions) - Venantonio Canals: Speedboating"
    VENANTONIO_CANALS_VEHICLE_THREADING_THE_NEEDLE = "Venantonio (Special Missions) - Venantonio Canals: Threading the Needle"
    DAMS_EDGE_HYDRANO_VEHICLE_CHASING_A_LEAD = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Chasing a Lead"
    DAMS_EDGE_HYDRANO_VEHICLE_RUSH_HOUR = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Rush Hour"
    DAMS_EDGE_HYDRANO_VEHICLE_DRIVING_TEST = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Driving Test"
    GLACIARA_SKI_SLOPES_VEHICLE_VILLA_ESCAPE = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Villa Escape"
    GLACIARA_SKI_SLOPES_VEHICLE_BLACK_DIAMOND = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Black Diamond"
    GLACIARA_SKI_SLOPES_VEHICLE_GO_FOR_THE_GOLD = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Go for the Gold"


SPECIAL_CHALLENGE_FLAGS: dict[str, EventFlag] = {
    SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_GREAT_ESCAPE: EventFlag(0x206C9E, 0b00000001),
    SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_SPEEDBOATING: EventFlag(0x206C9F, 0b00000001),
    SACSpecialChallengeLocations.VENANTONIO_CANALS_VEHICLE_THREADING_THE_NEEDLE: EventFlag(0x206CA0, 0b00000001),
    SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_CHASING_A_LEAD: EventFlag(0x206CA1, 0b00000001),
    SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_RUSH_HOUR: EventFlag(0x206CA2, 0b00000001),
    SACSpecialChallengeLocations.DAMS_EDGE_HYDRANO_VEHICLE_DRIVING_TEST: EventFlag(0x206CA3, 0b00000001),
    SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_VILLA_ESCAPE: EventFlag(0x206C9B, 0b00000001),
    SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_BLACK_DIAMOND: EventFlag(0x206C9C, 0b00000001),
    SACSpecialChallengeLocations.GLACIARA_SKI_SLOPES_VEHICLE_GO_FOR_THE_GOLD: EventFlag(0x206C9D, 0b00000001),
}

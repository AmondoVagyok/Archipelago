"""Every SAC location as one SACLocation record (see model.py), defined in the case file (locations/<case>.py)
it belongs to -- this module only gathers them and exposes the per-category lookups other modules read."""
from .a_fiction_full_of_dollars import LOCATIONS as A_FICTION_FULL_OF_DOLLARS_LOCATIONS
from .asyanica_rooftops import LOCATIONS as ASYANICA_ROOFTOPS_LOCATIONS
from .azcotal_alley import LOCATIONS as AZCOTAL_ALLEY_LOCATIONS
from .boltaire_gem_wing import LOCATIONS as BOLTAIRE_GEM_WING_LOCATIONS
from .boltaire_museum import LOCATIONS as BOLTAIRE_MUSEUM_LOCATIONS
from .bulkhead_lock import LOCATIONS as BULKHEAD_LOCK_LOCATIONS
from .countess_villa import LOCATIONS as COUNTESS_VILLA_LOCATIONS
from .dams_edge_hydrano import LOCATIONS as DAMS_EDGE_HYDRANO_LOCATIONS
from .galactic_bolt_reserve import LOCATIONS as GALACTIC_BOLT_RESERVE_LOCATIONS
from .glaciara_ski_slopes import LOCATIONS as GLACIARA_SKI_SLOPES_LOCATIONS
from .gondola_ascent import LOCATIONS as GONDOLA_ASCENT_LOCATIONS
from .high_rollers_casino import LOCATIONS as HIGH_ROLLERS_CASINO_LOCATIONS
from .high_stakes_room import LOCATIONS as HIGH_STAKES_ROOM_LOCATIONS
from .inside_the_a_eye import LOCATIONS as INSIDE_THE_A_EYE_LOCATIONS
from .klunks_lair import LOCATIONS as KLUNKS_LAIR_LOCATIONS
from .larger_than_life import LOCATIONS as LARGER_THAN_LIFE_LOCATIONS
from .madam_butterqwark import LOCATIONS as MADAM_BUTTERQWARK_LOCATIONS
from .max_security_cells import LOCATIONS as MAX_SECURITY_CELLS_LOCATIONS
from .model import BASE_ID, SACLocation, SACLocationType
from .prison_breakout import LOCATIONS as PRISON_BREAKOUT_LOCATIONS
from .rooftop_deathtrap import LOCATIONS as ROOFTOP_DEATHTRAP_LOCATIONS
from .saint_qwark import LOCATIONS as SAINT_QWARK_LOCATIONS
from .spaceship_graveyard import LOCATIONS as SPACESHIP_GRAVEYARD_LOCATIONS
from .suck_and_jive import LOCATIONS as SUCK_AND_JIVE_LOCATIONS
from .the_exercise_yard import LOCATIONS as THE_EXERCISE_YARD_LOCATIONS
from .the_mess_hall import LOCATIONS as THE_MESS_HALL_LOCATIONS
from .the_quasar_fields import LOCATIONS as THE_QUASAR_FIELDS_LOCATIONS
from .the_showers import LOCATIONS as THE_SHOWERS_LOCATIONS
from .underwater_bunker import LOCATIONS as UNDERWATER_BUNKER_LOCATIONS
from .vendors import (BASE_VENDOR_LOCATIONS as _BASE_VENDOR,
                      MOD_VENDOR_LOCATIONS as _MOD_VENDOR, TITAN_VENDOR_LOCATIONS as _TITAN_VENDOR)
from .venantonio_canals import LOCATIONS as VENANTONIO_CANALS_LOCATIONS
from .venantonio_labs import LOCATIONS as VENANTONIO_LABS_LOCATIONS
from .weapon_levels import WEAPON_LEVEL_LOCATIONS
from .nanotech import NANOTECH_LOCATIONS
from .stealth import STEALTH_TAKEDOWN_LOCATIONS

__all__ = [
    "ALIEN_CODE_LOCATIONS", "ALL_LOCATIONS", "BASE_ID", "CASE_LOCATIONS", "KEYCARD_LOCATIONS", "LOCATIONS",
    "MOD_VENDOR_LOCATIONS", "SACLocation", "SACLocationType", "SKILL_POINT_LOCATIONS", "TITAN_VENDOR_LOCATIONS",
    "TITANIUM_BOLT_LOCATIONS",
]

# case_id order.
CASE_LOCATIONS: tuple[SACLocation, ...] = (
    *BOLTAIRE_MUSEUM_LOCATIONS,
    *BOLTAIRE_GEM_WING_LOCATIONS,
    *MAX_SECURITY_CELLS_LOCATIONS,
    *ROOFTOP_DEATHTRAP_LOCATIONS,
    *ASYANICA_ROOFTOPS_LOCATIONS,
    *LARGER_THAN_LIFE_LOCATIONS,
    *COUNTESS_VILLA_LOCATIONS,
    *GLACIARA_SKI_SLOPES_LOCATIONS,
    *THE_MESS_HALL_LOCATIONS,
    *AZCOTAL_ALLEY_LOCATIONS,
    *GONDOLA_ASCENT_LOCATIONS,
    *SUCK_AND_JIVE_LOCATIONS,
    *HIGH_ROLLERS_CASINO_LOCATIONS,
    *THE_EXERCISE_YARD_LOCATIONS,
    *HIGH_STAKES_ROOM_LOCATIONS,
    *VENANTONIO_LABS_LOCATIONS,
    *VENANTONIO_CANALS_LOCATIONS,
    *MADAM_BUTTERQWARK_LOCATIONS,
    *GALACTIC_BOLT_RESERVE_LOCATIONS,
    *INSIDE_THE_A_EYE_LOCATIONS,
    *THE_SHOWERS_LOCATIONS,
    *SPACESHIP_GRAVEYARD_LOCATIONS,
    *SAINT_QWARK_LOCATIONS,
    *THE_QUASAR_FIELDS_LOCATIONS,
    *PRISON_BREAKOUT_LOCATIONS,
    *DAMS_EDGE_HYDRANO_LOCATIONS,
    *A_FICTION_FULL_OF_DOLLARS_LOCATIONS,
    *BULKHEAD_LOCK_LOCATIONS,
    *UNDERWATER_BUNKER_LOCATIONS,
    *KLUNKS_LAIR_LOCATIONS,
)
LOCATIONS: tuple[SACLocation, ...] = (*CASE_LOCATIONS, *_BASE_VENDOR, *_TITAN_VENDOR, *_MOD_VENDOR,
                                    *WEAPON_LEVEL_LOCATIONS.values(), *NANOTECH_LOCATIONS.values(), *STEALTH_TAKEDOWN_LOCATIONS.values())


def _by_type(*types: SACLocationType) -> dict[str, SACLocation]:
    return {location.name: location for location in LOCATIONS if location.type in types}


ALL_LOCATIONS: dict[str, SACLocation] = {location.name: location for location in LOCATIONS}
TITANIUM_BOLT_LOCATIONS = _by_type(SACLocationType.TITANIUM_BOLT)
SKILL_POINT_LOCATIONS = _by_type(SACLocationType.SKILL_POINT)
KEYCARD_LOCATIONS = _by_type(SACLocationType.KEYCARD)
ALIEN_CODE_LOCATIONS = _by_type(SACLocationType.ALIEN_CODE)
TITAN_VENDOR_LOCATIONS = _by_type(SACLocationType.TITAN_VENDOR)
MOD_VENDOR_LOCATIONS = _by_type(SACLocationType.MOD_VENDOR)

BASE_VENDOR_LOCATIONS = _by_type(SACLocationType.VENDOR)

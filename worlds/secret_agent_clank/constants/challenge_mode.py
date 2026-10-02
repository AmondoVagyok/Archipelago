"""Challenge-mode item identity and shared shop requirements."""
from .vendor import NG_PLUS_VENDOR_ITEMS, vendor_location_name
from .weapon_mods import VENDOR_MODS
from .weapon_progression import TITAN_LOCATIONS

PROGRESSIVE_CHALLENGE_MODE = "Progressive Challenge Mode"
CHALLENGE_VENDOR_LOCATIONS = frozenset({
    *(vendor_location_name(name) for name in NG_PLUS_VENDOR_ITEMS),
    *(mod.location for mod in VENDOR_MODS if mod.ng_plus),
    *TITAN_LOCATIONS.values(),
})

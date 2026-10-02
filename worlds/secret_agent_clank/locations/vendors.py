"""One shared Agency vendor: base purchases, weapon mods, and Titan/Proto upgrades.
Numeric IDs are retained; corrected equipment names require regenerated seeds.
"""
from ..constants.clank_gadgets import SACClankGadgets, SACClankWeapons
from ..constants.weapons import SACRatchetWeapons
from ..constants.weapon_mods import VENDOR_MODS
from ..constants.weapon_progression import TITAN_LOCATIONS
from ..constants.vendor import vendor_location_name
from .model import BASE_ID, SACLocation, SACLocationType

TITAN_VENDOR_LOCATIONS: tuple[SACLocation, ...] = tuple(
    SACLocation(name, None, None, SACLocationType.TITAN_VENDOR, BASE_ID + 31000 + index)
    for index, name in enumerate(TITAN_LOCATIONS.values())
)

MOD_VENDOR_LOCATIONS: tuple[SACLocation, ...] = tuple(
    SACLocation(mod.location, None, None, SACLocationType.MOD_VENDOR, BASE_ID + 32000 + mod.mod_id)
    for mod in VENDOR_MODS
)

BASE_VENDOR_LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(vendor_location_name(SACClankGadgets.CLANKPDA), None, None, SACLocationType.VENDOR, 77_809_002),
    SACLocation(vendor_location_name(SACClankWeapons.HOLOKNUCKLES), None, None, SACLocationType.VENDOR, 77_800_003),
    SACLocation(vendor_location_name(SACClankWeapons.SUPERKICK), None, None, SACLocationType.VENDOR, 77_800_004),
    SACLocation(vendor_location_name(SACRatchetWeapons.PORKBOMB), None, None, SACLocationType.VENDOR, 77_812_000),
    SACLocation(vendor_location_name(SACClankGadgets.HYPNOWATCH), None, None, SACLocationType.VENDOR, 77_812_001),
    SACLocation(vendor_location_name(SACRatchetWeapons.SHOCKROCKET), None, None, SACLocationType.VENDOR, 77_819_000),
    SACLocation(vendor_location_name(SACClankGadgets.BOLTGRABBER), None, None, SACLocationType.VENDOR, 77_819_001),
    SACLocation(vendor_location_name(SACRatchetWeapons.RYNO), None, None, SACLocationType.VENDOR, 77_829_000),
    SACLocation(vendor_location_name(SACClankWeapons.KICKSPLOSION), None, None, SACLocationType.VENDOR, 77_829_001),
    SACLocation(vendor_location_name(SACRatchetWeapons.PLASMAWHIP), None, None, SACLocationType.VENDOR, 77_815_000),
    SACLocation(vendor_location_name(SACRatchetWeapons.KICKBLAST), None, None, SACLocationType.VENDOR, 77_815_001),
    SACLocation(vendor_location_name(SACClankWeapons.LIGHTNINGUMBRELLA), None, None, SACLocationType.VENDOR, 77_815_003),
)

"""One shared Agency vendor: base purchases, weapon mods, and Titan/Proto upgrades."""
from ..constants.clank_gadgets import SACClankGadgets, SACClankWeapons
from ..constants.vendor import vendor_location_name
from ..constants.weapon_mods import VENDOR_MODS
from ..constants.weapon_progression import TITAN_LOCATIONS
from ..constants.weapons import SACRatchetWeapons
from .model import SACLocation, SACLocationType

TITAN_VENDOR_LOCATIONS: tuple[SACLocation, ...] = tuple(
    SACLocation(name, SACLocationType.TITAN_VENDOR)
    for name in TITAN_LOCATIONS.values()
)

MOD_VENDOR_LOCATIONS: tuple[SACLocation, ...] = tuple(
    SACLocation(mod.location, SACLocationType.MOD_VENDOR)
    for mod in VENDOR_MODS
)

BASE_VENDOR_LOCATIONS: tuple[SACLocation, ...] = (
    SACLocation(vendor_location_name(SACClankGadgets.CLANKPDA), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankWeapons.HOLOKNUCKLES), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankWeapons.SUPERKICK), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACRatchetWeapons.PORKBOMB), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankGadgets.HYPNOWATCH), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACRatchetWeapons.SHOCKROCKET), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankGadgets.BOLTGRABBER), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACRatchetWeapons.RYNO), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankWeapons.KICKSPLOSION), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACRatchetWeapons.PLASMAWHIP), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACRatchetWeapons.KICKBLAST), SACLocationType.VENDOR),
    SACLocation(vendor_location_name(SACClankWeapons.LIGHTNINGUMBRELLA), SACLocationType.VENDOR),
)

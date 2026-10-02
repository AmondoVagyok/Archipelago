"""SAC's single shop, reached from Clank's pause menu.

Base offers live here; weapon mods and Titan/Proto upgrades are in weapon_mods.py and
weapon_progression.py. All of them share the "Vendor: <item>" location naming.
"""
from dataclasses import dataclass

from .clank_gadgets import SACClankGadgets, SACClankWeapons
from .weapons import SACRatchetWeapons

VENDOR_LOCATION_PREFIX = "Vendor: "


def vendor_location_name(display_name: str) -> str:
    return f"{VENDOR_LOCATION_PREFIX}{display_name}"


@dataclass(frozen=True)
class SACVendorWeapons:
    """Equipment whose only native source is the vendor."""
    SHOCKROCKET       = SACRatchetWeapons.SHOCKROCKET
    PLASMAWHIP        = SACRatchetWeapons.PLASMAWHIP
    PORKBOMB          = SACRatchetWeapons.PORKBOMB
    RYNO              = SACRatchetWeapons.RYNO
    KICKBLAST         = SACRatchetWeapons.KICKBLAST
    HOLOKNUCKLES      = SACClankWeapons.HOLOKNUCKLES
    LIGHTNINGUMBRELLA = SACClankWeapons.LIGHTNINGUMBRELLA
    SUPERKICK         = SACClankWeapons.SUPERKICK
    KICKSPLOSION      = SACClankWeapons.KICKSPLOSION
    HYPNOWATCH        = SACClankGadgets.HYPNOWATCH
    CLANKPDA          = SACClankGadgets.CLANKPDA
    BOLTGRABBER       = SACClankGadgets.BOLTGRABBER


VENDOR_WEAPONS: tuple[str, ...] = tuple(
    value for name, value in vars(SACVendorWeapons).items() if not name.startswith("_")
)

# Purchases introduced only in challenge mode.
NG_PLUS_VENDOR_ITEMS = frozenset({SACRatchetWeapons.RYNO, SACClankWeapons.KICKSPLOSION})

"""Clank item names."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SACClankWeapons:
    """WEAPON_ORDER-struct Clank items that have a progressive counterpart (see SACProgressiveClankWeapons) -- see module docstring for the split from SACClankGadgets' lock/unlock-only items."""
    THROWTIE          = "Weapon: Clank: Bowtie"
    CUFFLINK          = "Weapon: Clank: Cufflink"
    TANGLEVINE        = "Weapon: Clank: Tanglevine"
    FLAMETHROWERPEN   = "Weapon: Clank: Flamethrower Briefcase"
    HOLOKNUCKLES      = "Weapon: Clank: HoloKnuckles"
    SUPERKICK         = "Weapon: Clank: Superkick"
    LIGHTNINGUMBRELLA = "Weapon: Clank: Umbrella"
    KICKSPLOSION      = "Weapon: Clank: Kicksplosion"


@dataclass(frozen=True)
class SACProgressiveClankWeapons:
    """Progressive-item counterpart to SACClankWeapons."""
    THROWTIE          = "Progressive: Clank: Bowtie"
    CUFFLINK          = "Progressive: Clank: Cufflink"
    TANGLEVINE        = "Progressive: Clank: Tanglevine"
    FLAMETHROWERPEN   = "Progressive: Clank: Flamethrower Briefcase"
    HOLOKNUCKLES      = "Progressive: Clank: HoloKnuckles"
    LIGHTNINGUMBRELLA = "Progressive: Clank: Umbrella"


@dataclass(frozen=True)
class SACClankGadgets:
    """Lock/unlock-only Clank items (no progression) -- see module docstring for why the two mechanically-separate tracking systems (case_id-keyed CLANK_GADGET_BY_CASE_ID vs the shared WEAPON_ORDER struct) share one naming class."""

    BLACK_OUT_PEN      = "Gadget: Clank: Black Out Pen"
    THERM_OPTIC_SHADES = "Gadget: Clank: Therm-Optic Shades"
    CLANKPDA           = "Gadget: Clank: PDA"
    JETBOOTS           = "Gadget: Clank: Jet Boots"
    OMNIKEY            = "Gadget: Clank: Omnikey"
    HYPNOWATCH         = "Gadget: Clank: Hypnowatch"
    HOLOMONOCLE        = "Gadget: Clank: Holomonocle"
    BOLTGRABBER        = "Gadget: Clank: Boltgrabber"


# Case_id -> gadget names for the positional (non-WEAPON_ORDER) Clank gadget
# system -- keyed by case_id rather than a plain tuple position so a gap
# (no confirmed gadget at case_id 2/3) doesn't require every later entry to
# shift, unlike the old CLANK_GADGETS tuple this replaces. Both Black Out Pen
# and Therm-Optic Shades are picked up in Boltaire Museum -- CONFIRMED.
CLANK_GADGET_BY_CASE_ID: dict[int, tuple[str, ...]] = {
    1: (SACClankGadgets.BLACK_OUT_PEN, SACClankGadgets.THERM_OPTIC_SHADES),  # Boltaire Museum
}

# Flat tuple for items/__init__.py's _table() -- iteration order matches
# CLANK_GADGET_BY_CASE_ID's insertion order (Python dicts preserve it).
CLANK_GADGETS: tuple[str, ...] = tuple(
    gadget for gadgets in CLANK_GADGET_BY_CASE_ID.values() for gadget in gadgets
)


@dataclass(frozen=True)
class SACGadgetPickupLocations:
    BOLTAIRE_MUSEUM_BLACK_OUT_PEN = 'Gadget: Clank: Black Out Pen (Pickup)'
    BOLTAIRE_MUSEUM_THERM_OPTIC_SHADES = 'Gadget: Clank: Therm-Optic Shades (Pickup)'

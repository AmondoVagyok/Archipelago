"""Ratchet's weapons/tools, sourced from the single 40-slot WeaponData struct
array core/weapons.py's WEAPON_ORDER documents.

Character split: WEAPON_ORDER is one shared struct array, but its contents
are NOT all Ratchet's:
  - SACRatchetWeapons: Ratchet's own real, obtainable weapons/tools.
  - constants/clank_gadgets.py's SACClankGadgets/SACClankWeapons: Clank's
    items that live in this same struct -- see that module's docstring for
    the gadgets(no progression)/weapons(has progression) split.
  - SACQwarkWeapons: Qwark's own slots -- documentation only, not wired
    into the randomizer at all.

Display names: every SACRatchetWeapons/SACClankGadgets/SACClankWeapons
WEAPON_ORDER-struct value is "Weapon:/Gadget: {Character}: {name}".
*_DISPLAY_TO_INTERNAL below maps back to the raw WEAPON_ORDER name, used by
core/core.py.

Filtering: WEAPON_ORDER has 40 slots; excluded entirely (not real,
obtainable, in-game content):
  - slot 0, 1: blank / unnamed.
  - Vacuum(20), hypershot(22), mapomatic(34), boxbreaker(36),
    wrenchpower_firebomb/triplewave/crystallix/wildburst(28-31): unused/
    unreachable content.
  - sunglasses(25): TODO -- believed to be the same physical unlock as
    constants/clank_gadgets.py's THERM_OPTIC_SHADES; not yet reconciled.
  - fountainpen(17): believed to be the same physical unlock as
    constants/clank_gadgets.py's Black Out Pen (GadgetData slot 17);
    left out here to avoid double-counting.

Postgame/Challenge Mode content is included: ryno (RYNO, 2,000,000 bolts),
kicksplosion (Hot Foot 2.1 Beta, 200,000 bolts, now Clank's -- see
clank_gadgets.py).

See WEAPONS_BY_CASE/GADGETS_BY_CASE below for where each of these becomes an
AP location.

Weapon mods have their own catalog in constants/weapon_mods.py. Native
vendor transaction flags are separate from AP ownership;
core/weapon_mods.py handles those hooks.
"""
from dataclasses import dataclass

from .clank_gadgets import SACClankGadgets, SACClankWeapons


@dataclass(frozen=True)
class SACRatchetWeapons:
    SHOCKROCKET       = "Weapon: Ratchet: Shock Rocket"
    PLASMAWHIP        = "Weapon: Ratchet: Plasma Whip"
    PORKBOMB          = "Weapon: Ratchet: Porkbomb"
    KICKBLAST         = "Weapon: Ratchet: Kickblast"
    BLASTER           = "Weapon: Ratchet: Lacerator"
    SHARDGUN          = "Weapon: Ratchet: Shardgun"
    BEEMINEGLOVE      = "Weapon: Ratchet: Beemineglove"
    WALLOPER          = "Weapon: Ratchet: Walloper"
    MINELAUNCHER      = "Weapon: Ratchet: Minelauncher"
    RATCHETPDA        = "Weapon: Ratchet: Ratchet PDA"
    BOLTTRANSFER      = "Weapon: Ratchet: Bolttransfer"
    RYNO              = "Weapon: Ratchet: Ryno"


@dataclass(frozen=True)
class SACProgressiveRatchetWeapons:
    SHOCKROCKET       = "Progressive: Ratchet: Shockrocket"
    PLASMAWHIP        = "Progressive: Ratchet: Plasmawhip"
    PORKBOMB          = "Progressive: Ratchet: Porkbomb"
    BLASTER           = "Progressive: Ratchet: Lacerator"
    SHARDGUN          = "Progressive: Ratchet: Shardgun"
    BEEMINEGLOVE      = "Progressive: Ratchet: Beemineglove"
    WALLOPER          = "Progressive: Ratchet: Walloper"
    MINELAUNCHER      = "Progressive: Ratchet: Minelauncher"
    RATCHETPDA        = "Progressive: Ratchet: Ratchetpda"
    BOLTTRANSFER      = "Progressive: Ratchet: Bolttransfer"
    RYNO              = "Progressive: Ratchet: Ryno"


@dataclass(frozen=True)
class SACQwarkWeapons:
    """We are not including Qwarks weapons in AP tool just for noting"""
    QWARKBLASTER      = "QwarkBlaster"
    GIANTQWARKBLASTER = "GiantQwarkBlaster"


# Display name -> WEAPON_ORDER internal name (core/weapons.py) -- used by
# core/core.py every tick to translate WeaponInventory.check()'s raw
# results before send_location().
RATCHET_WEAPON_DISPLAY_TO_INTERNAL: dict[str, str] = {
    SACRatchetWeapons.SHOCKROCKET:       "shockrocket",
    SACRatchetWeapons.PLASMAWHIP:        "plasmawhip",
    SACRatchetWeapons.PORKBOMB:          "porkbomb",
    SACRatchetWeapons.KICKBLAST:         "kickblast",
    SACRatchetWeapons.BLASTER:           "blaster",
    SACRatchetWeapons.SHARDGUN:          "shardgun",
    SACRatchetWeapons.BEEMINEGLOVE:      "beemineglove",
    SACRatchetWeapons.WALLOPER:          "walloper",
    SACRatchetWeapons.MINELAUNCHER:      "minelauncher",
    SACRatchetWeapons.RATCHETPDA:        "ratchetpda",
    SACRatchetWeapons.BOLTTRANSFER:      "bolttransfer",
    SACRatchetWeapons.RYNO:              "ryno",
}
RATCHET_WEAPON_INTERNAL_TO_DISPLAY: dict[str, str] = {v: k for k, v in RATCHET_WEAPON_DISPLAY_TO_INTERNAL.items()}

# WEAPON_ORDER-struct half of Clank's items (constants/clank_gadgets.py) --
# both SACClankGadgets (lock/unlock-only) and SACClankWeapons (has
# progression) combined, since world.py only needs to know "is this
# WEAPON_ORDER slot Clank's", not which of the two naming classes it's in.
GADGET_DISPLAY_TO_INTERNAL: dict[str, str] = {
    SACClankGadgets.CLANKPDA:        "clankpda",
    SACClankGadgets.JETBOOTS:        "jetboots",
    SACClankGadgets.OMNIKEY:         "omnikey",
    SACClankGadgets.HYPNOWATCH:      "hypnowatch",
    SACClankGadgets.HOLOMONOCLE:     "holomonocle",
    SACClankGadgets.BOLTGRABBER:     "boltgrabber",
    SACClankWeapons.THROWTIE:          "throwTie",
    SACClankWeapons.CUFFLINK:          "CuffLink",
    SACClankWeapons.TANGLEVINE:        "TangleVine",
    SACClankWeapons.FLAMETHROWERPEN:   "FlamethrowerPen",
    SACClankWeapons.HOLOKNUCKLES:      "HoloKnuckles",
    SACClankWeapons.SUPERKICK:         "superkick",
    SACClankWeapons.LIGHTNINGUMBRELLA: "LightningUmbrella",
    SACClankWeapons.KICKSPLOSION:      "kicksplosion",
}
GADGET_INTERNAL_TO_DISPLAY: dict[str, str] = {v: k for k, v in GADGET_DISPLAY_TO_INTERNAL.items()}

# Flat tuples for items/__init__.py's _table().
RATCHET_WEAPONS: tuple[str, ...] = tuple(RATCHET_WEAPON_DISPLAY_TO_INTERNAL)
GADGETS_FROM_WEAPON_TABLE: tuple[str, ...] = tuple(GADGET_DISPLAY_TO_INTERNAL)

# Mapping of each SACRatchetWeapons entry to the SACCases case its AP
# location lives in.
# STATUS: LOW CONFIDENCE -- expect individual entries to move once verified
# live (e.g. via /force_case + checking what that case's vendor/level offers).
WEAPONS_BY_CASE: dict[str, tuple[str, ...]] = {
    "Boltaire Museum": (
        SACRatchetWeapons.BLASTER,
    ),
    "Max-Security Cells": (
        SACRatchetWeapons.SHARDGUN, SACRatchetWeapons.WALLOPER,
    ),
    "Rooftop Deathtrap": (
        SACRatchetWeapons.MINELAUNCHER,
    ),
    "Azcotal Alley": (
        SACRatchetWeapons.BEEMINEGLOVE,
    ),
    "High-Rollers Casino": (
        SACRatchetWeapons.PORKBOMB,
    ),
    "Venantonio Labs": (
        SACRatchetWeapons.PLASMAWHIP, SACRatchetWeapons.KICKBLAST,
    ),
    "Inside the A-Eye": (
        SACRatchetWeapons.SHOCKROCKET,
    ),
    "Klunk's Lair": (
        SACRatchetWeapons.RYNO,
    ),
}

# Same shape/confidence caveat as WEAPONS_BY_CASE above, for the Clank
# items that live in this same WEAPON_ORDER struct -- case placements
# carried over unchanged from when these were (mis)classified as Ratchet
# weapons in WEAPONS_BY_CASE, not re-derived.
GADGETS_BY_CASE: dict[str, tuple[str, ...]] = {
    "Boltaire Museum": (
        SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS,
        SACClankWeapons.HOLOKNUCKLES, SACClankWeapons.SUPERKICK,
    ),
    "Rooftop Deathtrap": (
        SACClankWeapons.CUFFLINK, SACClankGadgets.OMNIKEY,
    ),
    "Azcotal Alley": (
        SACClankWeapons.TANGLEVINE, SACClankGadgets.CLANKPDA,
    ),
    "High-Rollers Casino": (
        SACClankGadgets.HYPNOWATCH, SACClankGadgets.HOLOMONOCLE,
    ),
    "Venantonio Labs": (
        SACClankWeapons.FLAMETHROWERPEN, SACClankWeapons.LIGHTNINGUMBRELLA,
    ),
    "Inside the A-Eye": (
        SACClankGadgets.BOLTGRABBER,
    ),
    "Klunk's Lair": (
        SACClankWeapons.KICKSPLOSION,
    ),
}

"""Ratchet's (and a handful of Clank's) weapons/tools, sourced from the single
40-slot WeaponData struct array core/weapons.py's WEAPON_ORDER documents --
see that module for the live-confirmed struct layout every name below must
stay byte-for-byte identical to (core/core.py's WeaponInventory.check() keys
its results by these exact strings, and core/core.py translates them to the
display names below before calling send_location()).

Real content, researched from GameFAQs' PS2 Secret Agent Clank weapon guide
(https://gamefaqs.gamespot.com/ps2/958888-secret-agent-clank/faqs/64306)
and the Fandom "Secret Agent Clank vendors" page
(https://ratchetandclank.fandom.com/wiki/Secret_Agent_Clank_vendors),
cross-referenced slot-by-slot against core/weapons.py's WEAPON_ORDER table.

Character split
----------------
WEAPON_ORDER is one shared struct array, but its contents are NOT all
Ratchet's -- some slots are Clank's spy gadgets and Qwark's own weapons,
just tracked in the same table:
  - SACRatchetWeapons: Ratchet's own real, obtainable weapons/tools (18).
  - constants/clank_gadgets.py's SACClankGadgets: Clank's spy gadgets that
    live in this same struct (8) -- clankpda, throwTie, CuffLink,
    TangleVine, FlamethrowerPen, jetboots, HoloKnuckles, superkick (user:
    "jetboots is a clank gadget", "this is also a clank weapon same with
    super kick" re: HoloKnuckles/superkick). SACClankGadgets ALSO holds 4
    more items from a mechanically separate, positional-by-case-id system
    (constants/clank_gadgets.py's own CLANK_GADGETS list) -- merged into one
    naming class since gadgets are Clank-only (user: "there are no gadgets
    for the other characters"), even though the two groups are tracked by
    different game memory structures (WEAPON_ORDER struct vs the positional
    list) and stay in separate item tables (WEAPON_ITEM_TABLE/
    case.ratchet_items vs GADGET_ITEM_TABLE/case.clank_items -- see
    items/__init__.py).
  - SACQwarkWeapons: Qwark's own 3 slots (19-21) -- documentation only, not
    wired into the randomizer at all (no items, no locations, no rules
    reference these). They exist purely so the full 40-slot table is
    accounted for somewhere in constants/, not because Qwark content is
    planned to be playable/randomized.

Display names
-------------
Every SACRatchetWeapons/SACClankGadgets WEAPON_ORDER-struct value is "Unlock:
{Character} {internal name}" -- same Unlock:/Progressive: layout as
rac_size_matters' Rac5Weapons/Rac5ProgressiveWeapons. The {internal name} half
is left as the exact WEAPON_ORDER string (e.g. "shockrocket") rather than an
invented pretty name ("Shock Rocket") -- no display-name translation layer
exists anywhere else in this client, and keeping the raw internal name means
every item/location string stays directly, unambiguously traceable back to
the exact game slot it represents. *_DISPLAY_TO_INTERNAL below is the
(trivial, prefix-strip) mapping back to that raw name, used by core/core.py.

Filtering: WEAPON_ORDER has 40 slots. Excluded entirely (not real, obtainable,
in-game content per the two sources above, and left out of every class below
so none of them ever becomes a randomizer item at all):
  - slot 0, 1: blank / unnamed (see core/weapons.py's WEAPON_ORDER comment).
  - Vacuum(20): no mention in either source -- unused/unreachable content,
    despite living next to the two real Qwark slots; NOT included in
    SACQwarkWeapons for that reason (only QwarkBlaster/GiantQwarkBlaster are).
  - hypershot(22), mapomatic(34), boxbreaker(36): no mention in either source
    -- unused/unreachable content.
  - sunglasses(25): believed to be the SAME physical unlock as
    constants/clank_gadgets.py's already-tracked THERM_OPTIC_SHADES (used by
    the Alien Codes goal) -- deliberately left out to avoid minting a second,
    separate AP item for what is likely one in-game thing. Reconciling which
    of the two systems actually backs Therm-Optic Shades is a separate,
    not-yet-done investigation.
  - fountainpen(17): believed to be the SAME physical unlock as
    constants/clank_gadgets.py's already-confirmed Black Out Pen (GadgetData
    slot 17, internal name fountainpen -- see that module's docstring). Left
    out of SACClankGadgets' WEAPON_ORDER-struct group for the same reason
    sunglasses is left out of SACRatchetWeapons: it already has a real
    location/item via clank_gadgets.py's positional CLANK_GADGETS list, and
    minting a second one here would double-count the same pickup.
  - wrenchpower_firebomb/triplewave/crystallix/wildburst(28-31): no mention
    in either source -- unused/unreachable content.

Postgame / Challenge Mode content is explicitly INCLUDED (not excluded) per
user instruction -- postgame content is real randomizer content: ryno (RYNO,
2,000,000 bolts), kicksplosion (Hot Foot 2.1 Beta, 200,000 bolts).

See WEAPONS_BY_CASE/GADGETS_BY_CASE below for where each of these becomes an
AP location.

Weapon mods have their own catalog in constants/weapon_mods.py: 16 Ratchet
mods and three postgame Clank mods. Native vendor transaction flags are
separate from AP ownership; core/weapon_mods.py handles those hooks.
"""
from dataclasses import dataclass

from .clank_gadgets import SACClankGadgets


@dataclass(frozen=True)
class SACRatchetWeapons:
    """Ratchet's own real, obtainable weapons/tools -- see module docstring
    for the Unlock: layout and why Clank's/Qwark's WEAPON_ORDER slots are
    excluded from this class specifically."""
    SHOCKROCKET       = "Unlock: Ratchet shockrocket"
    PLASMAWHIP        = "Unlock: Ratchet plasmawhip"
    PORKBOMB          = "Unlock: Ratchet porkbomb"
    LIGHTNINGUMBRELLA = "Unlock: Ratchet LightningUmbrella"
    HYPNOWATCH        = "Unlock: Ratchet hypnowatch"
    BOLTGRABBER       = "Unlock: Ratchet boltgrabber"
    KICKBLAST         = "Unlock: Ratchet kickblast"
    BLASTER           = "Unlock: Ratchet blaster"
    SHARDGUN          = "Unlock: Ratchet shardgun"
    BEEMINEGLOVE      = "Unlock: Ratchet beemineglove"
    WALLOPER          = "Unlock: Ratchet walloper"
    MINELAUNCHER      = "Unlock: Ratchet minelauncher"
    OMNIKEY           = "Unlock: Ratchet omnikey"
    RATCHETPDA        = "Unlock: Ratchet ratchetpda"
    HOLOMONOCLE       = "Unlock: Ratchet holomonocle"
    BOLTTRANSFER      = "Unlock: Ratchet bolttransfer"
    RYNO              = "Unlock: Ratchet ryno"
    KICKSPLOSION      = "Unlock: Ratchet kicksplosion"


@dataclass(frozen=True)
class SACProgressiveRatchetWeapons:
    """Progressive-item counterpart to SACRatchetWeapons, "Progressive: Ratchet
    {internal name}" -- naming-layout scaffolding only (see module docstring's
    TODO); not currently pooled by world.py or wired to any option."""
    SHOCKROCKET       = "Progressive: Ratchet shockrocket"
    PLASMAWHIP        = "Progressive: Ratchet plasmawhip"
    PORKBOMB          = "Progressive: Ratchet porkbomb"
    LIGHTNINGUMBRELLA = "Progressive: Ratchet LightningUmbrella"
    HYPNOWATCH        = "Progressive: Ratchet hypnowatch"
    BOLTGRABBER       = "Progressive: Ratchet boltgrabber"
    KICKBLAST         = "Progressive: Ratchet kickblast"
    BLASTER           = "Progressive: Ratchet blaster"
    SHARDGUN          = "Progressive: Ratchet shardgun"
    BEEMINEGLOVE      = "Progressive: Ratchet beemineglove"
    WALLOPER          = "Progressive: Ratchet walloper"
    MINELAUNCHER      = "Progressive: Ratchet minelauncher"
    OMNIKEY           = "Progressive: Ratchet omnikey"
    RATCHETPDA        = "Progressive: Ratchet ratchetpda"
    HOLOMONOCLE       = "Progressive: Ratchet holomonocle"
    BOLTTRANSFER      = "Progressive: Ratchet bolttransfer"
    RYNO              = "Progressive: Ratchet ryno"
    KICKSPLOSION      = "Progressive: Ratchet kicksplosion"


@dataclass(frozen=True)
class SACQwarkWeapons:
    """Qwark's own WEAPON_ORDER slots (19, 21 -- slot 20/Vacuum has no mention
    in either research source, see module docstring, so it's left out even
    though it sits between these two). Documentation only, per user
    instruction: these "are not going to do anything in the randomizer, its
    more documentation". No items, no locations, no rules reference these.
    Left as raw internal names (no Unlock:/Progressive: wrapping) since
    they're not real AP item/location strings."""
    QWARKBLASTER      = "QwarkBlaster"
    GIANTQWARKBLASTER = "GiantQwarkBlaster"


# Display name -> WEAPON_ORDER internal name (core/weapons.py) -- a trivial
# strip of the fixed "Unlock: Ratchet "/"Unlock: Clank " prefix, but kept as an
# explicit table (rather than re-deriving it with string slicing at every call
# site) since core/core.py needs it every tick to translate
# WeaponInventory.check()'s raw results before send_location().
RATCHET_WEAPON_DISPLAY_TO_INTERNAL: dict[str, str] = {
    SACRatchetWeapons.SHOCKROCKET:       "shockrocket",
    SACRatchetWeapons.PLASMAWHIP:        "plasmawhip",
    SACRatchetWeapons.PORKBOMB:          "porkbomb",
    SACRatchetWeapons.LIGHTNINGUMBRELLA: "LightningUmbrella",
    SACRatchetWeapons.HYPNOWATCH:        "hypnowatch",
    SACRatchetWeapons.BOLTGRABBER:       "boltgrabber",
    SACRatchetWeapons.KICKBLAST:         "kickblast",
    SACRatchetWeapons.BLASTER:           "blaster",
    SACRatchetWeapons.SHARDGUN:          "shardgun",
    SACRatchetWeapons.BEEMINEGLOVE:      "beemineglove",
    SACRatchetWeapons.WALLOPER:          "walloper",
    SACRatchetWeapons.MINELAUNCHER:      "minelauncher",
    SACRatchetWeapons.OMNIKEY:           "omnikey",
    SACRatchetWeapons.RATCHETPDA:        "ratchetpda",
    SACRatchetWeapons.HOLOMONOCLE:       "holomonocle",
    SACRatchetWeapons.BOLTTRANSFER:      "bolttransfer",
    SACRatchetWeapons.RYNO:              "ryno",
    SACRatchetWeapons.KICKSPLOSION:      "kicksplosion",
}
RATCHET_WEAPON_INTERNAL_TO_DISPLAY: dict[str, str] = {v: k for k, v in RATCHET_WEAPON_DISPLAY_TO_INTERNAL.items()}

# WEAPON_ORDER-struct half of SACClankGadgets (constants/clank_gadgets.py) --
# see that module's docstring for why these share a naming class with the
# positional CLANK_GADGETS system despite living in this different struct.
GADGET_DISPLAY_TO_INTERNAL: dict[str, str] = {
    SACClankGadgets.CLANKPDA:        "clankpda",
    SACClankGadgets.THROWTIE:        "throwTie",
    SACClankGadgets.CUFFLINK:        "CuffLink",
    SACClankGadgets.TANGLEVINE:      "TangleVine",
    SACClankGadgets.FLAMETHROWERPEN: "FlamethrowerPen",
    SACClankGadgets.JETBOOTS:        "jetboots",
    SACClankGadgets.HOLOKNUCKLES:    "HoloKnuckles",
    SACClankGadgets.SUPERKICK:       "superkick",
}
GADGET_INTERNAL_TO_DISPLAY: dict[str, str] = {v: k for k, v in GADGET_DISPLAY_TO_INTERNAL.items()}

# Flat tuples for items/__init__.py's _table() -- iteration order matches the
# dicts above (Python dicts preserve insertion order).
RATCHET_WEAPONS: tuple[str, ...] = tuple(RATCHET_WEAPON_DISPLAY_TO_INTERNAL)
GADGETS_FROM_WEAPON_TABLE: tuple[str, ...] = tuple(GADGET_DISPLAY_TO_INTERNAL)

# Best-effort mapping of each SACRatchetWeapons/SACClankGadgets (WEAPON_ORDER
# half) entry to the SACCases case its AP location lives in -- see
# locations/<case>.py's use of these two tables (replaces the old "one
# placeholder weapon per case index" scheme) and constants/planets.py's
# Case/CASES_BY_PLANET for the underlying case data.
#
# Every entry here is placed at its planet's EARLIEST case
# (CASES_BY_PLANET[planet][0]) as a simplification -- the real in-game
# vendor/pickup may actually sit in a later case of the same planet.
# "Arena prize" items (the source material names no specific planet) are
# placed at Max-Security Cells (Prison Planet's earliest case) as a
# best-guess combat-arena location. Postgame/Challenge Mode items are placed
# at Klunk's Lair (constants/planets.py's GOAL_CASE, the last case) as a
# stand-in for "only reachable after finishing the story".
#
# STATUS: LOW CONFIDENCE, same caveat as constants/planets.py's own
# planet/case guesses (several of which are themselves flagged LOW
# CONFIDENCE) -- expect individual entries to move once verified live (e.g.
# via /force_case + actually checking what that case's vendor/level offers).
# Keyed by SACCases display name (constants/planets.py), not case_id, since
# that's what locations/<case>.py's _CASE_NAME already is.
WEAPONS_BY_CASE: dict[str, tuple[str, ...]] = {
    "Boltaire Museum": (
        SACRatchetWeapons.BLASTER,
    ),
    "Max-Security Cells": (
        SACRatchetWeapons.SHARDGUN, SACRatchetWeapons.WALLOPER,
    ),
    "Rooftop Deathtrap": (
        SACRatchetWeapons.MINELAUNCHER, SACRatchetWeapons.OMNIKEY,
    ),
    "Azcotal Alley": (
        SACRatchetWeapons.BEEMINEGLOVE,
    ),
    "High-Rollers Casino": (
        SACRatchetWeapons.PORKBOMB, SACRatchetWeapons.HYPNOWATCH, SACRatchetWeapons.HOLOMONOCLE,
    ),
    "Venantonio Labs": (
        SACRatchetWeapons.PLASMAWHIP, SACRatchetWeapons.LIGHTNINGUMBRELLA, SACRatchetWeapons.KICKBLAST,
    ),
    "Inside the A-Eye": (
        SACRatchetWeapons.SHOCKROCKET, SACRatchetWeapons.BOLTGRABBER,
    ),
    "Klunk's Lair": (
        SACRatchetWeapons.RYNO, SACRatchetWeapons.KICKSPLOSION,
    ),
}

# Same shape/confidence caveat as WEAPONS_BY_CASE above, for the 8 Clank
# gadgets that live in this same WEAPON_ORDER struct -- case placements
# carried over unchanged from when these were (mis)classified as Ratchet
# weapons in WEAPONS_BY_CASE, not re-derived.
GADGETS_BY_CASE: dict[str, tuple[str, ...]] = {
    "Boltaire Museum": (
        SACClankGadgets.THROWTIE, SACClankGadgets.JETBOOTS,
        SACClankGadgets.HOLOKNUCKLES, SACClankGadgets.SUPERKICK,
    ),
    "Rooftop Deathtrap": (
        SACClankGadgets.CUFFLINK,
    ),
    "Azcotal Alley": (
        SACClankGadgets.TANGLEVINE, SACClankGadgets.CLANKPDA,
    ),
    "Venantonio Labs": (
        SACClankGadgets.FLAMETHROWERPEN,
    ),
}

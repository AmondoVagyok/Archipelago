"""Clank item names.

Black Out Pen is GadgetData slot 17 (internal name fountainpen), verified
against the running USA game and GADGET_PlayerHasGadget's code on 2026-09-11.
Core merges its AP entitlement into the shared 32-bit ownership table.
Its physical delivery/pickup state is separate and is still being mapped.

The Boltaire Gem Wing/Max-Security Cells placeholder gadgets were removed
(user: "the placeholder gadgets should be removed as they are not in the
game we have actual gadgets now" -- the 8 real WEAPON_ORDER-struct gadgets
below cover Clank's actual gadget roster) -- CLANK_GADGET_BY_CASE_ID now
only has the 2 confirmed positional entries, keyed by case_id rather than
tuple position, so removing the gap doesn't require every other entry to
shift.

SACClankGadgets is the single naming home for every gadget Clank owns (user:
"there are no gadgets for the other characters" -- gadgets are Clank-only, so
there's no reason to split them across two differently-named classes just
because they're tracked by two different memory structures). It holds both:
  - The 2 items below (BLACK_OUT_PEN, THERM_OPTIC_SHADES), keyed by case_id
    via CLANK_GADGET_BY_CASE_ID below -- backs GADGET_ITEM_TABLE/
    case.clank_items.
  - 8 more (CLANKPDA, THROWTIE, CUFFLINK, TANGLEVINE, FLAMETHROWERPEN,
    JETBOOTS, HOLOKNUCKLES, SUPERKICK) that mechanically live in the same
    40-slot WEAPON_ORDER struct as Ratchet's weapons (see core/weapons.py,
    constants/weapons.py's own docstring) -- backs WEAPON_ITEM_TABLE/
    case.ratchet_items instead. This used to be a separate SACGadgets class
    in constants/weapons.py; merged here since the split was an
    implementation detail, not something the naming needed to expose.
    GADGETS_FROM_WEAPON_TABLE/GADGET_DISPLAY_TO_INTERNAL/GADGETS_BY_CASE in
    constants/weapons.py still build the WEAPON_ORDER-side tracking tables
    from these same attributes.
"""
from dataclasses import dataclass

from .planets import CASE_ID_TO_CASE


@dataclass(frozen=True)
class SACClankGadgets:
    """String constants for every gadget Clank owns -- see module docstring
    for why the two mechanically-separate tracking systems (case_id-keyed
    CLANK_GADGET_BY_CASE_ID vs the shared WEAPON_ORDER struct) share one
    naming class."""

    BLACK_OUT_PEN = "Black Out Pen"
    THERM_OPTIC_SHADES = "Therm-Optic Shades"

    # WEAPON_ORDER-struct gadgets -- see constants/weapons.py's
    # GADGETS_FROM_WEAPON_TABLE/GADGET_DISPLAY_TO_INTERNAL/GADGETS_BY_CASE.
    CLANKPDA         = "Unlock: Clank PDA"
    THROWTIE         = "Unlock: Clank Bowtie"
    CUFFLINK         = "Unlock: Clank Cufflink"
    TANGLEVINE       = "Unlock: Clank Tanglevine"
    FLAMETHROWERPEN  = "Unlock: Clank Flamethrower Briefcase"
    JETBOOTS         = "Unlock: Clank jetboots"
    HOLOKNUCKLES     = "Unlock: Clank HoloKnuckles"
    SUPERKICK        = "Unlock: Clank superkick"


@dataclass(frozen=True)
class SACProgressiveClankGadgets:
    """Progressive-item counterpart to SACClankGadgets' WEAPON_ORDER-struct
    entries, "Progressive: Clank {internal name}" -- naming-layout
    scaffolding only (see constants/weapons.py's TODO); not currently
    pooled by world.py or wired to any option."""

    THROWTIE         = "Progressive: Clank throwTie"
    CUFFLINK         = "Progressive: Clank CuffLink"
    TANGLEVINE       = "Progressive: Clank TangleVine"
    FLAMETHROWERPEN  = "Progressive: Clank FlamethrowerPen"
    JETBOOTS         = "Progressive: Clank jetboots"
    HOLOKNUCKLES     = "Progressive: Clank HoloKnuckles"
    SUPERKICK        = "Progressive: Clank superkick"


# Back-compat aliases -- existing callers (rule_helpers.py, regions.py,
# items/__init__.py) import these two flat names directly.
BLACK_OUT_PEN = SACClankGadgets.BLACK_OUT_PEN
THERM_OPTIC_SHADES = SACClankGadgets.THERM_OPTIC_SHADES

# Case_id -> gadget name for the positional (non-WEAPON_ORDER) Clank gadget
# system -- keyed by case_id rather than a plain tuple position so a gap
# (no confirmed gadget at case_id 2/3) doesn't require every later entry to
# shift, unlike the old CLANK_GADGETS tuple this replaces.
CLANK_GADGET_BY_CASE_ID: dict[int, str] = {
    1: SACClankGadgets.BLACK_OUT_PEN,        # Boltaire Museum -- CONFIRMED, see docstring
    4: SACClankGadgets.THERM_OPTIC_SHADES,   # Rooftop Deathtrap
}

# Flat tuple for items/__init__.py's _table() -- iteration order matches
# CLANK_GADGET_BY_CASE_ID's insertion order (Python dicts preserve it).
CLANK_GADGETS: tuple[str, ...] = tuple(CLANK_GADGET_BY_CASE_ID.values())

# Case name -> that case's "{gadget} (Pickup)" location name, derived from
# CLANK_GADGET_BY_CASE_ID above (see locations/<case>.py's identical
# `f"{CLANK_GADGET_BY_CASE_ID[_CASE_ID]} (Pickup)"` construction) -- lets
# rules/<case>.py reference this location by constant instead of
# hand-typing the same string a second time.
GADGET_PICKUP_BY_CASE: dict[str, str] = {
    CASE_ID_TO_CASE[case_id].name: f"{gadget} (Pickup)"
    for case_id, gadget in CLANK_GADGET_BY_CASE_ID.items()
    if case_id in CASE_ID_TO_CASE
}


@dataclass(frozen=True)
class SACGadgetPickupLocations:
    """One named constant per "{gadget} (Pickup)" location -- same values
    as GADGET_PICKUP_BY_CASE, spelled out here so rules/<case>.py can
    reference an individual location directly instead of a case-name-keyed
    lookup -- same one-name-per-location layout as constants/weapons.py's
    SACRatchetWeapons."""

    BOLTAIRE_MUSEUM = "Black Out Pen (Pickup)"
    ROOFTOP_DEATHTRAP = "Therm-Optic Shades (Pickup)"

assert {v for k, v in vars(SACGadgetPickupLocations).items() if not k.startswith("_")} == set(
    GADGET_PICKUP_BY_CASE.values()
), "SACGadgetPickupLocations drifted out of sync with GADGET_PICKUP_BY_CASE -- regenerate its literals"

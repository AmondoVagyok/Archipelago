"""Item tables."""
from typing import NamedTuple

from BaseClasses import ItemClassification

from ..constants import (
    CASE_NAME_TO_INFOBOT,
    CHARACTER_ITEM_NAME,
    CLANK_GADGETS,
    GADGETS_FROM_WEAPON_TABLE,
    PLANET_ACCESS_ITEM_NAME,
    PROGRESSIVE_CHARACTER_ITEM_NAME,
    RATCHET_WEAPONS,
    SACCheats,
    SACTraps,
)

BASE_ID = 77_800_000

PROGRESSIVE_PLANET_ITEM_NAME = "Progressive Planet"


class SACItemData(NamedTuple):
    code: int
    classification: ItemClassification


_next_id = BASE_ID

def _table(names: tuple[str, ...], classification: ItemClassification) -> dict[str, SACItemData]:
    global _next_id
    table: dict[str, SACItemData] = {}
    for name in names:
        table[name] = SACItemData(_next_id, classification)
        _next_id += 1
    return table


WEAPON_ITEM_TABLE: dict[str, SACItemData] = _table(RATCHET_WEAPONS, ItemClassification.progression)
# constants/clank_gadgets.py's SACClankGadgets holds two mechanically
# different groups (see that class's docstring): 8 items (clankpda/throwTie/
# CuffLink/TangleVine/FlamethrowerPen/jetboots/HoloKnuckles/superkick) that
# are thematically Clank's, but mechanically live in the SAME WEAPON_ORDER
# struct Ratchet's own weapons live in -- core/core.py's case.ratchet_items
# tracks them, and client/context.py's `ratchet` ownership dict is what
# core/core.py's apply_inventory() expects them in, so they belong in
# WEAPON_ITEM_TABLE, NOT GADGET_ITEM_TABLE below (that table feeds the
# separate `clank` dict, for SACClankGadgets' other 2 items -- BLACK_OUT_PEN/
# THERM_OPTIC_SHADES -- an unrelated, positional Clank inventory system).
WEAPON_ITEM_TABLE.update(_table(GADGETS_FROM_WEAPON_TABLE, ItemClassification.progression))
# constants/weapons.py's RATCHET_WEAPONS no longer includes fountainpen/sunglasses at
# all (they're documented there as the same physical unlock as Black Out Pen/
# Therm-Optic Shades below) -- no popping needed here anymore.
GADGET_ITEM_TABLE: dict[str, SACItemData] = _table(CLANK_GADGETS, ItemClassification.progression)

# Planet access -- two alternative granularities, selected by options.py's
# Infobots choice (world.py's create_items() only ever pools ONE of these
# three tables, never more than one):
#   planets:    PLANET_ACCESS_ITEM_TABLE, one item per planet (coarse).
#   cases:      INFOBOT_ITEM_TABLE, one item per case (fine).
# Progressive Planet option additionally replaces PLANET_ACCESS_ITEM_TABLE
# with repeated copies of a single PROGRESSIVE_PLANET_ITEM_NAME item, each
# copy unlocking the next planet in PLANET_NAMES order -- see world.py.
PLANET_ACCESS_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(PLANET_ACCESS_ITEM_NAME.values()), ItemClassification.progression,
)
INFOBOT_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(CASE_NAME_TO_INFOBOT.values()), ItemClassification.progression,
)
PROGRESSIVE_PLANET_ITEM_TABLE: dict[str, SACItemData] = _table(
    (PROGRESSIVE_PLANET_ITEM_NAME,), ItemClassification.progression,
)

# Character Items option: Ratchet/Clank get one flat unlock item each;
# Qwark/Gadgetbots are progressive (user: "progressive characters
# specifically for qwark and gadgetbots") -- world.py pools multiple copies
# of each, one per case that character operates (see
# constants/planets.py's CASES_BY_OPERATIVE).
CHARACTER_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(CHARACTER_ITEM_NAME.values()), ItemClassification.progression,
)
PROGRESSIVE_CHARACTER_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(PROGRESSIVE_CHARACTER_ITEM_NAME.values()), ItemClassification.progression,
)

# Directly grants the "Ratchet Pack" vanilla cheat -- useful, not required
# for anything, so it's not progression.
RATCHET_PACK_ITEM_TABLE: dict[str, SACItemData] = _table((SACCheats.RATCHET_PACK,), ItemClassification.useful)

# Trap items -- force a vanilla cheat on for a duration when received (see
# constants/cheats.py's TRAP_CHEATS/TRAP_DURATIONS). Actual cheat-toggling
# in game memory is still a TODO (CHEATS_ADDRESS layout unconfirmed, see
# core/traps.py).
TRAP_ITEM_TABLE: dict[str, SACItemData] = _table(
    (SACTraps.WEAPON_SWITCHING, SACTraps.MIRRORED_LEVELS, SACTraps.BOLT_CONFUSION, SACTraps.BIG_HEADED),
    ItemClassification.trap,
)

FILLER_ITEM_NAME = "Bolts"
FILLER_ITEM_TABLE: dict[str, SACItemData] = _table((FILLER_ITEM_NAME,), ItemClassification.filler)

# Allocate after existing items to preserve every prior item ID.
PROGRESSIVE_WRENCH_ITEM_NAME = "Progressive Wrench"
PROGRESSIVE_WRENCH_ITEM_TABLE = _table((PROGRESSIVE_WRENCH_ITEM_NAME,), ItemClassification.progression)
for _mod in ("wrenchpower_firebomb", "wrenchpower_triplewave", "wrenchpower_crystallix", "wrenchpower_wildburst"):
    WEAPON_ITEM_TABLE.pop(_mod, None)

from ..constants.weapon_progression import PROGRESSIVE_TO_INTERNAL

PROGRESSIVE_WEAPON_ITEM_TABLE = _table(tuple(PROGRESSIVE_TO_INTERNAL), ItemClassification.progression)
from ..constants.weapon_progression import TITAN_ITEMS

# Retain IDs for compatibility with experimental seeds; new seeds use the
# automatic V4-to-V5 bridge and never pool separate Titan Upgrade items.
TITAN_ITEM_TABLE = _table(tuple(TITAN_ITEMS), ItemClassification.progression)

ALL_ITEMS: dict[str, SACItemData] = {
    **TITAN_ITEM_TABLE,
    **PROGRESSIVE_WEAPON_ITEM_TABLE,
    **PROGRESSIVE_WRENCH_ITEM_TABLE,
    **WEAPON_ITEM_TABLE,
    **GADGET_ITEM_TABLE,
    **PLANET_ACCESS_ITEM_TABLE,
    **INFOBOT_ITEM_TABLE,
    **PROGRESSIVE_PLANET_ITEM_TABLE,
    **CHARACTER_ITEM_TABLE,
    **PROGRESSIVE_CHARACTER_ITEM_TABLE,
    **RATCHET_PACK_ITEM_TABLE,
    **TRAP_ITEM_TABLE,
    **FILLER_ITEM_TABLE,
}

from ..constants.weapon_mods import WEAPON_MODS

WEAPON_MOD_ITEM_TABLE = _table(tuple(mod.name for mod in WEAPON_MODS), ItemClassification.useful)
ALL_ITEMS.update(WEAPON_MOD_ITEM_TABLE)

# Append so all existing item IDs remain stable.
from ..constants.challenge_mode import PROGRESSIVE_CHALLENGE_MODE
CHALLENGE_MODE_ITEM_TABLE = _table((PROGRESSIVE_CHALLENGE_MODE,), ItemClassification.progression)
ALL_ITEMS.update(CHALLENGE_MODE_ITEM_TABLE)

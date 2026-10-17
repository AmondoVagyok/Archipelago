"""Item tables.

IDs are handed out sequentially in the order the tables below are built, so new
tables must only ever be appended at the end to keep every existing item ID stable.
"""
from itertools import count
from typing import NamedTuple

from BaseClasses import ItemClassification

from ..constants import (
    CASE_NAME_TO_INFOBOT,
    CLANK_GADGETS,
    GADGETS_FROM_WEAPON_TABLE,
    KEYCARD_ITEMS,
    PLANET_ACCESS_ITEM_NAME,
    PROGRESSIVE_CHALLENGE_MODE,
    PROGRESSIVE_CHARACTER_ITEM_NAME,
    PROGRESSIVE_PLANET_ITEM_NAME,
    PROGRESSIVE_TO_INTERNAL,
    RATCHET_WEAPONS,
    TITAN_ITEMS,
    WEAPON_MODS,
    SACCheats,
    SACTraps,
)

BASE_ID = 77_800_000


class SACItemData(NamedTuple):
    code: int
    classification: ItemClassification


_next_id = count(BASE_ID)


def _table(names: tuple[str, ...], classification: ItemClassification) -> dict[str, SACItemData]:
    return {name: SACItemData(next(_next_id), classification) for name in names}


WEAPON_ITEM_TABLE: dict[str, SACItemData] = _table(RATCHET_WEAPONS, ItemClassification.progression)
WEAPON_ITEM_TABLE.update(_table(GADGETS_FROM_WEAPON_TABLE, ItemClassification.progression))
GADGET_ITEM_TABLE: dict[str, SACItemData] = _table(CLANK_GADGETS, ItemClassification.progression)

PLANET_ACCESS_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(PLANET_ACCESS_ITEM_NAME.values()), ItemClassification.progression,
)
INFOBOT_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(CASE_NAME_TO_INFOBOT.values()), ItemClassification.progression,
)
PROGRESSIVE_PLANET_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(PROGRESSIVE_PLANET_ITEM_NAME.values()), ItemClassification.progression,
)

PROGRESSIVE_CHARACTER_ITEM_TABLE: dict[str, SACItemData] = _table(
    tuple(PROGRESSIVE_CHARACTER_ITEM_NAME.values()), ItemClassification.progression,
)

RATCHET_PACK_ITEM_TABLE: dict[str, SACItemData] = _table((SACCheats.RATCHET_PACK,), ItemClassification.useful)

TRAP_ITEM_TABLE: dict[str, SACItemData] = _table(
    (SACTraps.WEAPON_SWITCHING, SACTraps.MIRRORED_LEVELS, SACTraps.BOLT_CONFUSION, SACTraps.BIG_HEADED),
    ItemClassification.trap,
)

FILLER_ITEM_NAME = "Bolts"
FILLER_ITEM_TABLE: dict[str, SACItemData] = _table((FILLER_ITEM_NAME,), ItemClassification.filler)

PROGRESSIVE_WRENCH_ITEM_NAME = "Progressive Wrench"
PROGRESSIVE_WRENCH_ITEM_TABLE = _table((PROGRESSIVE_WRENCH_ITEM_NAME,), ItemClassification.progression)
for _mod in ("wrenchpower_firebomb", "wrenchpower_triplewave", "wrenchpower_crystallix", "wrenchpower_wildburst"):
    WEAPON_ITEM_TABLE.pop(_mod, None)

PROGRESSIVE_WEAPON_ITEM_TABLE = _table(tuple(PROGRESSIVE_TO_INTERNAL), ItemClassification.progression)

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
    **PROGRESSIVE_CHARACTER_ITEM_TABLE,
    **RATCHET_PACK_ITEM_TABLE,
    **TRAP_ITEM_TABLE,
    **FILLER_ITEM_TABLE,
}

WEAPON_MOD_ITEM_TABLE = _table(tuple(mod.name for mod in WEAPON_MODS), ItemClassification.useful)
ALL_ITEMS.update(WEAPON_MOD_ITEM_TABLE)

CHALLENGE_MODE_ITEM_TABLE = _table((PROGRESSIVE_CHALLENGE_MODE,), ItemClassification.progression)
ALL_ITEMS.update(CHALLENGE_MODE_ITEM_TABLE)

KEYCARD_ITEM_TABLE = _table(tuple(KEYCARD_ITEMS), ItemClassification.progression)
ALL_ITEMS.update(KEYCARD_ITEM_TABLE)

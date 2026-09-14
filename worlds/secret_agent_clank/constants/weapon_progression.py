"""Only native multi-level weapons participate; tools stay single unlocks."""
from .clank_gadgets import SACClankWeapons, SACProgressiveClankWeapons
from .weapons import (
    GADGET_DISPLAY_TO_INTERNAL,
    RATCHET_WEAPON_DISPLAY_TO_INTERNAL,
    SACProgressiveRatchetWeapons,
    SACRatchetWeapons,
)

LEVELLED_INTERNALS = ("blaster", "shardgun", "beemineglove", "shockrocket",
    "walloper", "plasmawhip", "porkbomb", "minelauncher", "ryno", "throwTie",
    "CuffLink", "TangleVine", "HoloKnuckles", "FlamethrowerPen", "LightningUmbrella")


def _attrs(cls):
    return {name: value for name, value in vars(cls).items() if not name.startswith("_")}


# Unlock -> progressive display name, matched by shared class attribute name
# (e.g. SACRatchetWeapons.SHOCKROCKET <-> SACProgressiveRatchetWeapons.SHOCKROCKET)
# rather than string surgery on the display name itself, which broke once the
# "Unlock: {character} {weapon}" naming scheme was replaced by "Weapon:
# {character}: {weapon}" (see constants/weapons.py, constants/clank_gadgets.py).
_UNLOCK_ATTRS = {**_attrs(SACRatchetWeapons), **_attrs(SACClankWeapons)}
_PROGRESSIVE_ATTRS = {**_attrs(SACProgressiveRatchetWeapons), **_attrs(SACProgressiveClankWeapons)}
_DISPLAY_TO_INTERNAL = {**RATCHET_WEAPON_DISPLAY_TO_INTERNAL, **GADGET_DISPLAY_TO_INTERNAL}

UNLOCK_TO_PROGRESSIVE = {
    _UNLOCK_ATTRS[attr]: _PROGRESSIVE_ATTRS[attr]
    for attr in _PROGRESSIVE_ATTRS
    if attr in _UNLOCK_ATTRS and _DISPLAY_TO_INTERNAL.get(_UNLOCK_ATTRS[attr]) in LEVELLED_INTERNALS
}
PROGRESSIVE_TO_INTERNAL = {
    progressive: _DISPLAY_TO_INTERNAL[unlock] for unlock, progressive in UNLOCK_TO_PROGRESSIVE.items()
}
def max_level(internal, ng_plus):
    return 4 if internal == "ryno" or not ng_plus else 8

TITAN_LOCATIONS = {internal: f"Titan Vendor: {internal}"
                   for internal in LEVELLED_INTERNALS if internal != "ryno"}
TITAN_ITEMS = {f"Titan Upgrade: {internal}": internal for internal in TITAN_LOCATIONS}

from ...constants.clank_gadgets import SACClankGadgets
from ..inventories.weapons import WEAPON_ORDER, WeaponSlot

_VENDOR_SLOTS = (
    WeaponSlot.SHOCKROCKET, WeaponSlot.PLASMAWHIP, WeaponSlot.PORKBOMB, WeaponSlot.RYNO,
    WeaponSlot.HOLOKNUCKLES, WeaponSlot.LIGHTNINGUMBRELLA, WeaponSlot.HYPNOWATCH,
    WeaponSlot.CLANKPDA, WeaponSlot.BOLTGRABBER, WeaponSlot.SUPERKICK,
    WeaponSlot.KICKBLAST, WeaponSlot.KICKSPLOSION,
)
VENDOR_LOCATIONS = {slot: WEAPON_ORDER[slot] for slot in _VENDOR_SLOTS}

_PICKUP_SLOTS = (
    WeaponSlot.BLASTER, WeaponSlot.SHARDGUN, WeaponSlot.BEEMINEGLOVE, WeaponSlot.WALLOPER,
    WeaponSlot.MINELAUNCHER, WeaponSlot.THROWTIE, WeaponSlot.CUFFLINK, WeaponSlot.TANGLEVINE,
    WeaponSlot.FLAMETHROWERPEN,
    WeaponSlot.HOLOMONOCLE, WeaponSlot.JETBOOTS, WeaponSlot.OMNIKEY,
)
PICKUP_LOCATIONS = {slot: WEAPON_ORDER[slot] for slot in _PICKUP_SLOTS}
PICKUP_LOCATIONS[WeaponSlot.FOUNTAINPEN] = f"{SACClankGadgets.BLACK_OUT_PEN} (Pickup)"

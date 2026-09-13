"""Existing AP location names, separated by the native source of collection
-- consumed by patches/weapon_pickup.py and patches/vendor_only.py to build
their per-slot flag tables.

Values are pulled from WEAPON_ORDER via WeaponSlot rather than retyped by
hand, so a slot's name can never drift out of sync with its real internal
name (core/inventories/weapons.py is the single source of truth)."""
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
    # No RATCHETPDA: granted as the reward for The Showers' "No good deed
    # goes unpunished." Ratchet Challenge, not a separate native pickup
    # event -- that challenge's own location already covers this moment
    # (see constants/weapons.py's WEAPONS_BY_CASE, which no longer places
    # RATCHETPDA in any case).
    # No BOLTTRANSFER: granted as the reward for one of Prison Breakout!'s
    # Ratchet Challenges, not a separate native pickup event -- that
    # challenge's own location already covers this moment (see
    # constants/weapons.py's WEAPONS_BY_CASE, which no longer places
    # BOLTTRANSFER in any case).
    WeaponSlot.HOLOMONOCLE, WeaponSlot.JETBOOTS, WeaponSlot.OMNIKEY,
)
PICKUP_LOCATIONS = {slot: WEAPON_ORDER[slot] for slot in _PICKUP_SLOTS}
# FOUNTAINPEN's AP location uses the display name "Black Out Pen (Pickup)",
# not its WEAPON_ORDER internal name -- see constants/weapons.py's
# *_DISPLAY_TO_INTERNAL tables.
PICKUP_LOCATIONS[WeaponSlot.FOUNTAINPEN] = "Black Out Pen (Pickup)"

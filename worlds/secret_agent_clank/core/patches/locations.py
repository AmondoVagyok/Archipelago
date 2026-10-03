from ...constants.pickups import PICKUP_LOCATION_BY_INTERNAL
from ...constants.vendor import VENDOR_WEAPONS
from ...constants.weapon_order import WEAPON_ORDER, WeaponSlot
from ...constants.weapons import EQUIPMENT_DISPLAY_TO_INTERNAL

VENDOR_LOCATIONS = {
    WeaponSlot(WEAPON_ORDER.index(EQUIPMENT_DISPLAY_TO_INTERNAL[name])): EQUIPMENT_DISPLAY_TO_INTERNAL[name]
    for name in VENDOR_WEAPONS
}

_PICKUP_SLOTS = (
    WeaponSlot.BLASTER, WeaponSlot.SHARDGUN, WeaponSlot.BEEMINEGLOVE, WeaponSlot.WALLOPER,
    WeaponSlot.MINELAUNCHER, WeaponSlot.THROWTIE, WeaponSlot.CUFFLINK, WeaponSlot.TANGLEVINE,
    WeaponSlot.FLAMETHROWERPEN, WeaponSlot.FOUNTAINPEN,
    WeaponSlot.HOLOMONOCLE, WeaponSlot.JETBOOTS, WeaponSlot.OMNIKEY,
)
# Slot -> AP pickup location name the native hook reports.
PICKUP_LOCATIONS = {slot: PICKUP_LOCATION_BY_INTERNAL[WEAPON_ORDER[slot]] for slot in _PICKUP_SLOTS}

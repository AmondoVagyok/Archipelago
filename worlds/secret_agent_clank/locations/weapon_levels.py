"""Weapon level checks use a separate ID range; existing locations never move."""
from BaseClasses import Region

from ..constants import (
    EQUIPMENT_INTERNAL_TO_DISPLAY,
    LEVELLED_INTERNALS,
    NG_PLUS_VENDOR_ITEMS,
    SACOperatives,
    checked_levels,
    level_location_name,
)
from ..entities import SACLocation as Location
from ..options import enabled_operatives
from ..rules import VENDOR_ONLY_ITEM_NAMES, WeaponLevelRule
from .model import SACLocation, SACLocationType

WEAPON_LEVEL_LOCATIONS = {
    level_location_name(internal, level): SACLocation(
        level_location_name(internal, level), SACLocationType.WEAPON_LEVEL, WeaponLevelRule(internal, level),
    )
    for internal in LEVELLED_INTERNALS
    for level in checked_levels(internal, 4, 1)
}

def _enabled_weapons(world):
    """(internal, display name, operative) for every weapon whose levels are checks in this world."""
    for internal in LEVELLED_INTERNALS:
        name = EQUIPMENT_INTERNAL_TO_DISPLAY[internal]
        operative = SACOperatives.CLANK if name.endswith("(Clank)") else SACOperatives.RATCHET
        if operative not in enabled_operatives(world.options):
            continue
        if name in NG_PLUS_VENDOR_ITEMS and not world.options.ng_plus.value:
            continue
        if not world.has_vendor and name in VENDOR_ONLY_ITEM_NAMES:
            continue
        yield internal, name, operative


def create_weapon_level_locations(world, menu_region):
    mode = world.options.weapon_level_checks.value
    if not mode:
        return
    region = Region("Weapon Levels", world.player, world.multiworld)
    for internal, _name, _operative in _enabled_weapons(world):
        names = [level_location_name(internal, level)
                 for level in checked_levels(internal, mode, world.options.ng_plus.value)]
        region.add_locations({name: world.location_name_to_id[name] for name in names}, Location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

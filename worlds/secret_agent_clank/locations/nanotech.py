"""Clank-only health progression checks, with stable IDs across NG modes."""
from ..constants.nanotech import nanotech_levels, nanotech_location_name
from .model import BASE_ID, SACLocation, SACLocationType

NANOTECH_LOCATIONS = {
    nanotech_location_name(level): SACLocation(
        nanotech_location_name(level), None, None, SACLocationType.NANOTECH,
        BASE_ID + 34000 + level,
    ) for level in nanotech_levels(True)
}


def create_nanotech_locations(world, menu_region):
    from BaseClasses import Region
    from ..constants import SACOperatives
    from ..entities import SACLocation as Location
    from ..rules.nanotech import nanotech_access_rule

    if not world.options.nanotech_checks or SACOperatives.CLANK not in world.options.operatives.value:
        return
    region = Region("Clank Nanotech", world.player, world.multiworld)
    for level in nanotech_levels(world.options.ng_plus.value):
        definition = NANOTECH_LOCATIONS[nanotech_location_name(level)]
        location = Location(world.player, definition.name, definition.code, region)
        world.set_rule(location, nanotech_access_rule(world, level))
        region.locations.append(location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

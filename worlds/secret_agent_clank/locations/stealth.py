"""Cumulative successful Clank stealth takedown checks."""
from BaseClasses import Region

from ..constants import SACOperatives
from ..constants.stealth import stealth_location_name, stealth_thresholds
from ..entities import SACLocation as Location
from ..rules.stealth import stealth_access_rule
from .model import BASE_ID, SACLocation, SACLocationType

STEALTH_TAKEDOWN_LOCATIONS = {
    stealth_location_name(level): SACLocation(
        stealth_location_name(level), None, None, SACLocationType.STEALTH_TAKEDOWN,
        BASE_ID + 35000 + level,
    ) for level in range(1, 26)
}


def create_stealth_locations(world, menu_region):
    if not world.options.stealth_takedown_checks or SACOperatives.CLANK not in world.options.operatives.value:
        return
    region = Region("Clank Stealth Takedowns", world.player, world.multiworld)
    for level in stealth_thresholds(world.options.stealth_takedown_checks.value):
        definition = STEALTH_TAKEDOWN_LOCATIONS[stealth_location_name(level)]
        location = Location(world.player, definition.name, definition.code, region)
        world.set_rule(location, stealth_access_rule(world, level))
        region.locations.append(location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

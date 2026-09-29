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
    from rule_builder.rules import CanReachRegion, False_
    from ..constants import CASES_BY_OPERATIVE, SACOperatives
    from ..entities import SACLocation as Location

    if not world.options.nanotech_checks or SACOperatives.CLANK not in world.options.operatives.value:
        return
    region = Region("Clank Nanotech", world.player, world.multiworld)
    existing = {r.name for r in world.multiworld.get_regions(world.player)}
    access = False_()
    for case in CASES_BY_OPERATIVE[SACOperatives.CLANK]:
        if case.name in existing:
            access = access | CanReachRegion(case.name)
    for level in nanotech_levels(world.options.ng_plus.value):
        definition = NANOTECH_LOCATIONS[nanotech_location_name(level)]
        location = Location(world.player, definition.name, definition.code, region)
        world.set_rule(location, access)
        region.locations.append(location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

"""Per-operative health progression checks, with stable IDs across NG modes."""
from BaseClasses import Region

from ..constants import (
    SACOperatives,
    nanotech_levels,
    nanotech_location_name,
    ratchet_nanotech_levels,
    ratchet_nanotech_location_name,
)
from ..entities import SACLocation as Location
from ..options import enabled_operatives
from ..rules import ClankNanotechRule, RatchetNanotechRule
from .model import SACLocation, SACLocationType

NANOTECH_LOCATIONS = {
    nanotech_location_name(level): SACLocation(
        nanotech_location_name(level), SACLocationType.NANOTECH, ClankNanotechRule(level),
    ) for level in nanotech_levels(True)
}


def create_nanotech_locations(world, menu_region):
    if not world.options.nanotech_checks:
        return
    region = Region("Clank Nanotech", world.player, world.multiworld)
    names = [nanotech_location_name(level) for level in nanotech_levels(world.options.ng_plus.value)]
    region.add_locations({name: world.location_name_to_id[name] for name in names}, Location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

RATCHET_NANOTECH_LOCATIONS = {
    ratchet_nanotech_location_name(level): SACLocation(
        ratchet_nanotech_location_name(level), SACLocationType.NANOTECH, RatchetNanotechRule(level),
    ) for level in ratchet_nanotech_levels(True)
}


def create_ratchet_nanotech_locations(world, menu_region):
    if not world.options.ratchet_nanotech_checks or SACOperatives.RATCHET not in enabled_operatives(world.options):
        return
    region = Region("Ratchet Nanotech", world.player, world.multiworld)
    names = [ratchet_nanotech_location_name(level) for level in ratchet_nanotech_levels(world.options.ng_plus.value)]
    region.add_locations({name: world.location_name_to_id[name] for name in names}, Location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

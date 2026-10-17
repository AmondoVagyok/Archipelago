from BaseClasses import Region

from ..constants import STEALTH_CASES, STEALTH_MAX_PER_CASE, stealth_check_count, stealth_location_name
from ..entities import SACLocation as Location
from ..rules import StealthCaseRule, region_names
from .model import SACLocation, SACLocationType

STEALTH_TAKEDOWN_LOCATIONS = {
    stealth_location_name(case, count): SACLocation(
        stealth_location_name(case, count), SACLocationType.STEALTH_TAKEDOWN, StealthCaseRule(case),
    ) for case in STEALTH_CASES for count in range(1, STEALTH_MAX_PER_CASE + 1)
}


def stealth_case_counts(world):
    """Case -> stealth checks it gets in this world (only existing cases with at least one)."""
    if world.using_ut:
        return dict(world.passthrough.get("stealth_cases", {}))
    existing = region_names(world)
    counts = {case: stealth_check_count(case, world.options.stealth_takedown_checks.value)
              for case in STEALTH_CASES if case in existing}
    return {case: count for case, count in counts.items() if count}


def create_stealth_locations(world, menu_region):
    counts = stealth_case_counts(world)
    if not counts:
        return
    region = Region("Clank Stealth Takedowns", world.player, world.multiworld)
    for case, count in counts.items():
        names = [stealth_location_name(case, takedown) for takedown in range(1, count + 1)]
        region.add_locations({name: world.location_name_to_id[name] for name in names}, Location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

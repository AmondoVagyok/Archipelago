"""Weapon level checks use a separate ID range; existing locations never move."""
from BaseClasses import Region
from rule_builder.rules import CanReachRegion, False_, Has

from ..constants import CASES_BY_OPERATIVE, SACOperatives
from ..constants.challenge_mode import PROGRESSIVE_CHALLENGE_MODE
from ..constants.vendor import NG_PLUS_VENDOR_ITEMS
from ..constants.weapon_progression import (
    LEVELLED_INTERNALS,
    UNLOCK_TO_PROGRESSIVE,
    checked_levels,
    level_location_name,
)
from ..constants.weapons import EQUIPMENT_INTERNAL_TO_DISPLAY
from ..entities import SACLocation as Location
from ..rules.rule_helpers import HasEnemyAccess, region_names
from ..rules.vendor_access import VENDOR_ONLY_ITEM_NAMES
from .model import BASE_ID, SACLocation, SACLocationType

WEAPON_LEVEL_LOCATIONS = {
    level_location_name(internal, level): SACLocation(
        level_location_name(internal, level), None, None, SACLocationType.WEAPON_LEVEL,
        BASE_ID + 33000 + index * 8 + level - 2,
    )
    for index, internal in enumerate(LEVELLED_INTERNALS)
    for level in checked_levels(internal, 4, 1)
}

CLANK_WEAPON_LEVEL_CASES: dict[str, tuple[str, ...]] = {
    "throwTie": (),
    "CuffLink": (),
    "TangleVine": (),
    "HoloKnuckles": (),
    "FlamethrowerPen": (),
    "LightningUmbrella": (),
}


def create_weapon_level_locations(world, menu_region):
    mode = world.options.weapon_level_checks.value
    if not mode:
        return
    region = Region("Weapon Levels", world.player, world.multiworld)
    existing = region_names(world)
    for internal in LEVELLED_INTERNALS:
        name = EQUIPMENT_INTERNAL_TO_DISPLAY[internal]
        operative = SACOperatives.CLANK if name.endswith("(Clank)") else SACOperatives.RATCHET
        if operative not in world.options.operatives.value:
            continue
        if name in NG_PLUS_VENDOR_ITEMS and not world.options.ng_plus.value:
            continue
        if not world.has_vendor and name in VENDOR_ONLY_ITEM_NAMES:
            continue
        cases = CLANK_WEAPON_LEVEL_CASES.get(internal, ()) or tuple(
            case.name for case in CASES_BY_OPERATIVE[operative])
        access = False_()
        for case in cases:
            if case in existing:
                access = access | CanReachRegion(case)
        if operative == SACOperatives.CLANK:
            # Levelling a Clank weapon needs enemies to use it on.
            access = access & HasEnemyAccess(world)
        for level in checked_levels(internal, mode, world.options.ng_plus.value):
            definition = WEAPON_LEVEL_LOCATIONS[level_location_name(internal, level)]
            location = Location(world.player, definition.name, definition.code, region)
            weapon = (Has(UNLOCK_TO_PROGRESSIVE[name], level)
                      if world.options.progressive_weapons else Has(name))
            rule = access & weapon
            if world.options.progressive_challenge_mode and level > 4:
                rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
            world.set_rule(location, rule)
            region.locations.append(location)
    menu_region.connect(region)
    world.multiworld.regions.append(region)

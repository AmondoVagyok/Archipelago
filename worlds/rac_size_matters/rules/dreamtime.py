from typing import TYPE_CHECKING

from rule_builder.rules import HasAll

from ..constants import (
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ._helpers import HasChallengeMode, HasProjectileWeapon, weapon_enabled

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_dreamtime_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    _base = HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC)

    if world.options.skill_points.value >= 2:
        world.set_rule(mw.get_location(Rac5SkillPoints.DREAMTIME_FRIENDS, player), _base)
        world.set_rule(mw.get_location(Rac5SkillPoints.DREAMTIME_NIGHT_TERRORS, player), _base)

    if world.options.all_missions:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DREAMTIME_COMPLETE, player), _base)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DREAMTIME_SLEEPING_RATCHET, player), _base)

    world.set_rule(mw.get_location(Rac5TBolts.DREAMTIME_HAT, player), _base)
    world.set_rule(mw.get_location(Rac5TBolts.DREAMTIME_GARAGE, player), _base)
    world.set_rule(mw.get_location(Rac5TBolts.DREAMTIME_CRAB, player), _base & HasProjectileWeapon())

    world.set_rule(mw.get_location(Rac5Locations.DREAMTIME_CHESTPLATE, player), _base)

    if weapon_enabled(world, Rac5Weapons.SUCK_CANNON):
        world.set_rule(mw.get_location(Rac5VendorLocations.DREAMTIME_SUCK, player), _base)

    if world.options.challenge_mode.value >= 1:
        tier1 = HasChallengeMode(world, 1)
        world.set_rule(mw.get_location(Rac5Locations.DREAMTIME_HYPERBOREAN_CHESTPLATE, player), _base & tier1)
        if weapon_enabled(world, Rac5Weapons.SUCK_CANNON):
            world.set_rule(mw.get_location(Rac5TitanVendorLocations.DREAMTIME_SUCK_TITAN, player), _base & tier1)

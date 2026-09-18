from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, True_

from ..constants import (
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Infobots,
    Rac5Locations,
    Rac5ModVendorLocations,
    Rac5ShrinkRayGrindrail,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ..options import ShrinkRayOptions
from ._helpers import HasShrinkRayDoorAccess, HasChallengeMode, weapon_enabled

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_challax_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    _base   = HasShrinkRayDoorAccess(world) & Has(Rac5Gadgets.POLARIZER)
    _sprout = _base & Has(Rac5Gadgets.SPROUT_O_MATIC)

    if world.options.skill_points.value >= 2:
        world.set_rule(mw.get_location(Rac5SkillPoints.CHALLAX_MASTER, player), _sprout)

    if world.options.all_missions:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.CHALLAX_EXPLORE, player), _sprout)

    if world.options.giant_clank:
        if world.options.skill_points.value >= 2:
            world.set_rule(mw.get_location(Rac5SkillPoints.CHALLAX_VARMINTS, player), True_())
        if world.options.all_missions:
            world.set_rule(mw.get_location(Rac5CutsceneLocations.CHALLAX_CLANK, player), True_())
        world.set_rule(mw.get_location(Rac5Locations.CHALLAX_CHESTPLATE, player), True_())

    world.set_rule(mw.get_location(Rac5TBolts.CHALLAX_MECH_PAD, player), True_())
    world.set_rule(mw.get_location(Rac5TBolts.CHALLAX_ROOM, player), _base)
    world.set_rule(mw.get_location(Rac5TBolts.CHALLAX_PLANT, player), _sprout)

    world.set_rule(
        mw.get_location(Rac5Locations.CHALLAX_HELMET, player),
        _sprout | Has(Rac5Infobots.DAYNI_MOON),
    )

    _shrink_ray = HasShrinkRayDoorAccess(world)
    if weapon_enabled(world, Rac5Weapons.SNIPER_MINE):
        world.set_rule(mw.get_location(Rac5VendorLocations.CHALLAX_SNIPER, player), _shrink_ray)
    world.set_rule(mw.get_location(Rac5VendorLocations.CHALLAX_PDA, player), _shrink_ray)

    if weapon_enabled(world, Rac5Weapons.LACERATOR):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_LACERATOR_DOUBLE, player), _base)
    if weapon_enabled(world, Rac5Weapons.ACID_BOMB_GLOVE):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_ACID_BURN, player), _base)
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_ACID_EPOXY, player), _base)
    if weapon_enabled(world, Rac5Weapons.CONCUSSION_GUN):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_CONCUSSION_LOCK, player), _base)
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_CONCUSSION_CHARGE, player), _base)
    if weapon_enabled(world, Rac5Weapons.BEE_MINE_GLOVE):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_BEE_WORKER, player), _base)

    if world.options.shrink_ray_options.value == ShrinkRayOptions.option_locations:
        world.set_rule(mw.get_location(Rac5ShrinkRayGrindrail.CHALLAX_GRINDRAIL, player), _shrink_ray)

    if world.options.challenge_mode.value >= 1:
        tier1 = HasChallengeMode(world, 1)
        world.set_rule(mw.get_location(Rac5Locations.CHALLAX_HYPERBOREAN_HELMET, player), _sprout & tier1)
        if weapon_enabled(world, Rac5Weapons.SNIPER_MINE):
            world.set_rule(
                mw.get_location(Rac5TitanVendorLocations.CHALLAX_SNIPER_TITAN, player), _shrink_ray & tier1
            )
            world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_SNIPER_SMART_REFLECTOR, player), _base & tier1)
        if weapon_enabled(world, Rac5Weapons.SHOCK_ROCKET):
            world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_SHOCK_MULTI_LAUNCHER, player), _base & tier1)
        if weapon_enabled(world, Rac5Weapons.LASER_TRACER):
            world.set_rule(mw.get_location(Rac5ModVendorLocations.CHALLAX_LASER_PIERCE, player), _base & tier1)


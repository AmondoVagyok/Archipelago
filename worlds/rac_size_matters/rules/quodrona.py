from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, True_

from ..constants import (
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Infobots,
    Rac5ModVendorLocations,
    Rac5ShrinkRayGrindrail,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ..options import ShrinkRayOptions
from ._helpers import HasShrinkRayDoorAccess, HasChallengeMode, HasInfobot, weapon_enabled

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_quodrona_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    _checks = HasShrinkRayDoorAccess(world) & Has(Rac5Gadgets.HYPERSHOT)

    if world.options.skill_points.value >= 2:
        world.set_rule(mw.get_location(Rac5SkillPoints.QUODRONA_ELITE, player), _checks)
        world.set_rule(mw.get_location(Rac5SkillPoints.QUODRONA_STORM, player), _checks)

    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.QUODRONA_CLONE, player), _checks)
        world.set_rule(mw.get_location(Rac5CutsceneLocations.QUODRONA_CHASE, player), _checks)
        world.set_rule(mw.get_location(Rac5CutsceneLocations.QUODRONA_MECHA, player), _checks)
    if world.options.all_missions:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.QUODRONA_FIND, player), _checks)

    world.set_rule(mw.get_location(Rac5TBolts.QUODRONA_DUMMIES, player), _checks)

    world.set_rule(mw.get_location(Rac5CutsceneLocations.QUODRONA_GOAL, player), _checks)

    world.set_rule(
        mw.get_location("Quodrona Completed", player),
        _checks & HasInfobot(Rac5Infobots.QUODRONA),
    )

    if weapon_enabled(world, Rac5Weapons.LASER_TRACER):
        world.set_rule(mw.get_location(Rac5VendorLocations.QUODRONA_LASER, player), True_())

    if weapon_enabled(world, Rac5Weapons.AGENTS_OF_DOOM):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_AGENTS_LAUNCHER, player), True_())
    if weapon_enabled(world, Rac5Weapons.SCORCHER):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_SCORCHER_SPITFIRE, player), True_())
    if weapon_enabled(world, Rac5Weapons.SNIPER_MINE):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_SNIPER_SPLIT, player), True_())
    if weapon_enabled(world, Rac5Weapons.SHOCK_ROCKET):
        world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_SHOCK_LOCK, player), True_())
        world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_SHOCK_AFTER, player), True_())

    if world.options.shrink_ray_options.value == ShrinkRayOptions.option_locations:
        world.set_rule(
            mw.get_location(Rac5ShrinkRayGrindrail.QUODRONA_ENTRANCE, player), Has(Rac5Gadgets.SHRINK_RAY)
        )
        world.set_rule(
            mw.get_location(Rac5ShrinkRayGrindrail.QUODRONA_CLONE_TRAINING_ROOM, player), Has(Rac5Gadgets.SHRINK_RAY)
        )

    if world.options.challenge_mode.value >= 1:
        tier1 = HasChallengeMode(world, 1)
        if weapon_enabled(world, Rac5Weapons.LASER_TRACER):
            world.set_rule(mw.get_location(Rac5TitanVendorLocations.QUODRONA_LASER_TITAN, player), tier1)
            world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_LASER_RICOCHET, player), tier1)
        if weapon_enabled(world, Rac5Weapons.STATIC_BARRIER):
            world.set_rule(mw.get_location(Rac5ModVendorLocations.QUODRONA_STATIC_MIRAGE, player), tier1)

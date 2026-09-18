from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, True_

from ..constants import (
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations,
    Rac5SkillPoints,
    Rac5SkyboardChallenges,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ._helpers import HasChallengeMode, weapon_enabled

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_outpost_omega_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    _facility = HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC)

    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.OUTPOST_OMEGA_ENTER, player), _facility)
        world.set_rule(mw.get_location(Rac5CutsceneLocations.OUTPOST_OMEGA, player), _facility)
    if world.options.all_missions:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.OUTPOST_OMEGA_ESCAPE, player), _facility)

    if world.options.challenge_mode.value >= 1:
        if weapon_enabled(world, Rac5Weapons.BEE_MINE_GLOVE):
            world.set_rule(
                mw.get_location(Rac5TitanVendorLocations.OUTPOST_OMEGA_BEE_TITAN, player), HasChallengeMode(world, 1)
            )
    if world.options.challenge_mode.value >= 2:
        world.set_rule(
            mw.get_location(Rac5Locations.OUTPOST_OMEGA_CHAMELEON_GLOVES, player), HasChallengeMode(world, 2)
        )


def set_outpost_omega_two_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    if weapon_enabled(world, Rac5Weapons.BEE_MINE_GLOVE):
        world.set_rule(mw.get_location(Rac5VendorLocations.OUTPOST_OMEGA_BEE, player), True_())
    if world.options.enable_skyboard_challenge_skill_points:
        world.set_rule(mw.get_location(Rac5SkillPoints.OUTPOST_OMEGA_AWESOME, player), True_())

    if world.options.all_missions and world.options.skyboard_challenges.value >= 1:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.OUTPOST_OMEGA_REMATCH, player), True_())

    world.set_rule(mw.get_location(Rac5TBolts.OUTPOST_OMEGA_DREAM, player), True_())

    if world.options.skyboard_challenges.value >= 1:
        world.set_rule(mw.get_location(Rac5SkyboardChallenges.OUTPOST_OMEGA_VERTIGO, player), True_())
        world.set_rule(mw.get_location(Rac5SkyboardChallenges.OUTPOST_OMEGA_INTERIOR, player), True_())
        world.set_rule(mw.get_location(Rac5SkyboardChallenges.OUTPOST_OMEGA_DANGER, player), True_())
        world.set_rule(mw.get_location(Rac5SkyboardChallenges.OUTPOST_OMEGA_VORTEX, player), True_())

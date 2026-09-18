from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasAll, True_

from ..constants import (
    Rac5ClankChallenges,
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations,
    Rac5ShrinkRayGrindrail,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ..locations import enabled_clank_challenge_names
from ..options import ShrinkRayOptions
from ._helpers import HasShrinkRayDoorAccess, HasChallengeMode, HasProjectileWeapon, HasTitanPrereq, weapon_enabled

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_dayni_moon_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld

    _base       = Has(Rac5Gadgets.SPROUT_O_MATIC) & HasProjectileWeapon()
    _shrink_ray = _base & HasShrinkRayDoorAccess(world)

    if world.options.skill_points.value >= 1:
        world.set_rule(mw.get_location(Rac5SkillPoints.DAYNI_MOON_BOUNCY, player), _base)
    if world.options.skill_points.value >= 2:
        world.set_rule(mw.get_location(Rac5SkillPoints.DAYNI_MOON_WOOL_PROTEST, player), _base)
    if world.options.enable_clank_challenge_skill_points:
        world.set_rule(mw.get_location(Rac5SkillPoints.DAYNI_MOON_GLADIATOR, player), True_())

    if world.options.all_missions:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DAYNI_MOON, player), _base)
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DAYNI_MOON_LUNA, player), _base)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DAYNI_MOON_FIGHT1, player), _base)
        world.set_rule(mw.get_location(Rac5CutsceneLocations.DAYNI_MOON_FIGHT2, player), _base)

    world.set_rule(mw.get_location(Rac5TBolts.DAYNI_MOON_BARN, player), _base)
    world.set_rule(mw.get_location(Rac5TBolts.DAYNI_MOON_MIMIC, player), _shrink_ray)

    world.set_rule(mw.get_location(Rac5Locations.DAYNI_MOON_HELMET, player), _base)

    enabled_names = enabled_clank_challenge_names(dict(world.options.clank_challenge_groups.value))
    if world.options.clank_challenges.value >= 1:
        for name in (Rac5ClankChallenges.DAYNI_MOON_SHOWDOWN, Rac5ClankChallenges.DAYNI_MOON_INFINITE):
            if name in enabled_names:
                world.set_rule(mw.get_location(name, player), True_())

    if world.options.clank_challenges.value >= 2:
        for name in (
            Rac5ClankChallenges.DAYNI_MOON_CROWD, Rac5ClankChallenges.DAYNI_MOON_REVERSE,
            Rac5ClankChallenges.DAYNI_MOON_BRIDGE, Rac5ClankChallenges.DAYNI_MOON_LEAP,
            Rac5ClankChallenges.DAYNI_MOON_WELCOME, Rac5ClankChallenges.DAYNI_MOON_ROUND,
            Rac5ClankChallenges.DAYNI_MOON_VARIETY, Rac5ClankChallenges.DAYNI_MOON_SAWYER,
            Rac5ClankChallenges.DAYNI_MOON_SMASHER, Rac5ClankChallenges.DAYNI_MOON_TOURNAMENT,
            Rac5ClankChallenges.DAYNI_MOON_AROUND, Rac5ClankChallenges.DAYNI_MOON_LINE,
            Rac5ClankChallenges.DAYNI_MOON_HAY,
        ):
            if name in enabled_names:
                world.set_rule(mw.get_location(name, player), True_())

    if weapon_enabled(world, Rac5Weapons.SHOCK_ROCKET):
        world.set_rule(mw.get_location(Rac5VendorLocations.DAYNI_MOON_SHOCK, player), True_())
    world.set_rule(mw.get_location(Rac5VendorLocations.DAYNI_MOON_MAP, player), True_())

    if world.options.shrink_ray_options.value == ShrinkRayOptions.option_locations:
        world.set_rule(
            mw.get_location(
                Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE, player),
                And(
                    HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.SPROUT_O_MATIC, Rac5Gadgets.SPROUT_O_MATIC),
                    HasProjectileWeapon(),
                    ),
        )

    if world.options.challenge_mode.value >= 1:
        tier1 = HasChallengeMode(world, 1)
        if weapon_enabled(world, Rac5Weapons.MOOTATOR):
            world.set_rule(
                mw.get_location(Rac5TitanVendorLocations.DAYNI_MOON_MOOTATOR_TITAN, player),
                HasTitanPrereq(world, Rac5Weapons.MOOTATOR) & tier1,
            )
        if weapon_enabled(world, Rac5Weapons.SHOCK_ROCKET):
            world.set_rule(mw.get_location(Rac5TitanVendorLocations.DAYNI_MOON_SHOCK_TITAN, player), tier1)

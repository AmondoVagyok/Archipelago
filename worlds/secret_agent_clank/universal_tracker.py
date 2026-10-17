"""Universal Tracker support: restore options from slot_data when UT regenerates the world without a YAML."""
from typing import TYPE_CHECKING, Any

from .constants import SACOperatives

if TYPE_CHECKING:
    from .world import SecretAgentClankWorld


def setup_options_from_slot_data(world: "SecretAgentClankWorld") -> None:
    if not hasattr(world.multiworld, "re_gen_passthrough") or world.game not in world.multiworld.re_gen_passthrough:
        world.using_ut = False
        return
    world.using_ut = True
    passthrough: dict[str, Any] = world.multiworld.re_gen_passthrough[world.game]
    world.passthrough = passthrough

    world.options.infobots.value = passthrough["infobots"]
    world.options.operatives.value = {name: amount for name, amount in passthrough["operatives"].items()
                                      if name != SACOperatives.CLANK}
    world.options.all_missions.value = passthrough["all_missions"]
    world.options.all_cutscenes.value = bool(passthrough["all_cutscenes"])
    world.options.skill_points.value = passthrough["skill_points"]
    world.options.random_skill_points.value = int(passthrough["random_skill_points"])
    world.options.skill_point_count.value = passthrough["skill_point_count"]
    world.options.keycards_and_alien_codes.value = int(passthrough["keycards_and_alien_codes"])
    world.options.goal.value = passthrough["goal"]
    world.options.pick_and_mix_goals.value = set(passthrough["pick_and_mix_goals"])

    world.options.keycard_hunt.value = int(passthrough["keycard_hunt"])
    world.options.progressive_wrench.value = int(passthrough["progressive_wrench"])
    world.options.ng_plus.value = passthrough["ng_plus"]
    world.options.progressive_challenge_mode.value = int(passthrough["progressive_challenge_mode"])
    world.options.progressive_weapons.value = passthrough["progressive_weapons"]
    world.options.weapon_level_checks.value = passthrough["weapon_level_checks"]
    world.options.nanotech_checks.value = int(passthrough["nanotech_checks"])
    world.options.ratchet_nanotech_checks.value = int(passthrough["ratchet_nanotech_checks"])
    world.options.stealth_takedown_checks.value = passthrough["stealth_takedown_checks"]
    world.options.starting_weapons.value = passthrough["starting_weapons"]
    world.options.starting_gadgets.value = passthrough["starting_gadgets"]
    world.options.starting_bolts.value = passthrough["starting_bolts"]
    world.options.death_amnesty.value = passthrough["death_amnesty"]
    world.options.trap_chance.value = passthrough["trap_chance"]
    world.options.trap_weight.value = dict(passthrough["trap_weight"])
    world.options.trap_duration.value = dict(passthrough["trap_duration"])

    world.options.death_link.value = bool(passthrough["death_link"])
    world.options.weapon_xp_multiplier.value = passthrough["weapon_xp_multiplier"]
    world.options.health_xp_multiplier.value = passthrough["health_xp_multiplier"]
    world.options.bolt_multiplier.value = passthrough["bolt_multiplier"]

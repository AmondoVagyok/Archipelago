"""Galactic Bolt Reserve's per-location rules -- every location belonging to this case is set here explicitly (mirrors worlds/rac_size_matters/rules' per-planet files, one world.set_rule() call per location, grouped by which options.py toggle gates that location's category -- a location only exists in the multiworld at all when its category's option is on, so calling get_location() on it unguarded would raise)."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.alien_codes import SACAlienCodeLocations
from ..constants.clank_gadgets import THERM_OPTIC_SHADES
from ..constants.cutscenes import SACCutsceneLocations
from ..constants.missions import SACMissionLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..constants.titanium_bolts import SACTitaniumBoltLocations
from ..options import Missions
from .rule_helpers import HasGadget

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_galactic_bolt_reserve_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_1, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_2, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.GALACTIC_BOLT_RESERVE_3, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.GALACTIC_BOLT_RESERVE_HARD_CURRENCY, player), True_())
        world.set_rule(mw.get_location(SACMissionLocations.GALACTIC_BOLT_RESERVE_THE_BIG_HEIST, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.GALACTIC_BOLT_RESERVE_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.GALACTIC_BOLT_RESERVE_ENTER_CUTSCENE, player), True_())
        world.set_rule(mw.get_location(SACCutsceneLocations.GALACTIC_BOLT_RESERVE_COMPLETE_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_WITH_INTEREST, player), True_())
        world.set_rule(
            mw.get_location(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_ANDROIDS_IN_DISGUISE, player), True_(),
        )
        world.set_rule(mw.get_location(SACSkillPointLocations.GALACTIC_BOLT_RESERVE_VAULT_VAULT, player), True_())

    # Alien code (AllAlienCodes) -- also needs Therm-Optic Shades
    if world.options.all_alien_codes:
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_AVERYS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_LESLEYS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.GALACTIC_BOLT_RESERVE_DAVES_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )

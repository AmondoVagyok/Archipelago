"""Spaceship Graveyard's per-location rules -- every location belonging to this case is set here explicitly (mirrors worlds/rac_size_matters/rules' per-planet files, one world.set_rule() call per location, grouped by which options.py toggle gates that location's category -- a location only exists in the multiworld at all when its category's option is on, so calling get_location() on it unguarded would raise)."""
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


def set_spaceship_graveyard_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_1, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_2, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_3, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.SPACESHIP_GRAVEYARD_4, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.SPACESHIP_GRAVEYARD_TRACKING_THE_KINGPIN, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.SPACESHIP_GRAVEYARD_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.SPACESHIP_GRAVEYARD_ENTER_CUTSCENE, player), True_())
        world.set_rule(mw.get_location(SACCutsceneLocations.SPACESHIP_GRAVEYARD_COMPLETE_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE, player), True_())
        world.set_rule(mw.get_location(SACSkillPointLocations.SPACESHIP_GRAVEYARD_REVENANT, player), True_())

    # Alien code (AllAlienCodes) -- also needs Therm-Optic Shades
    if world.options.all_alien_codes:
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_MATTS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_KENS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.SPACESHIP_GRAVEYARD_JAREDS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )

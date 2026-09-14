"""Underwater Bunker's per-location rules -- every location belonging to this case is set here explicitly (mirrors worlds/rac_size_matters/rules' per-planet files, one world.set_rule() call per location, grouped by which options.py toggle gates that location's category -- a location only exists in the multiworld at all when its category's option is on, so calling get_location() on it unguarded would raise)."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.alien_codes import SACAlienCodeLocations
from ..constants.clank_gadgets import THERM_OPTIC_SHADES
from ..constants.missions import SACMissionLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..constants.titanium_bolts import SACTitaniumBoltLocations
from ..options import Missions
from .rule_helpers import HasGadget

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_underwater_bunker_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.UNDERWATER_BUNKER_1, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.UNDERWATER_BUNKER_CLANK_UNDER_GLASS, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.UNDERWATER_BUNKER_COMPLETE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.UNDERWATER_BUNKER_LEET_HAXXOR, player), True_())
        world.set_rule(mw.get_location(SACSkillPointLocations.UNDERWATER_BUNKER_RUST_PROOF, player), True_())
        world.set_rule(mw.get_location(SACSkillPointLocations.UNDERWATER_BUNKER_IM_NOT_THERE, player), True_())

    # Alien code (AllAlienCodes) -- also needs Therm-Optic Shades
    if world.options.all_alien_codes:
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.UNDERWATER_BUNKER_VESSUPS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.UNDERWATER_BUNKER_ADAMS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.UNDERWATER_BUNKER_JEFFS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )

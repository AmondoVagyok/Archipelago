"""High-Rollers Casino's per-location rules -- every location belonging to
this case is set here explicitly (mirrors worlds/rac_size_matters/rules'
per-planet files, one world.set_rule() call per location, grouped by
which options.py toggle gates that location's category -- a location
only exists in the multiworld at all when its category's option is on,
so calling get_location() on it unguarded would raise). Reaching the
case at all is already gated by its "To High-Rollers Casino" entrance (see
rules/entrances.py's set_entrance_rules()), so most locations just need
True_() here; alien code locations additionally need Therm-Optic Shades
on top."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.alien_codes import SACAlienCodeLocations
from ..constants.clank_gadgets import THERM_OPTIC_SHADES
from ..constants.cutscenes import SACCutsceneLocations
from ..constants.missions import SACMissionLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..constants.titanium_bolts import SACTitaniumBoltLocations
from ..constants.weapons import SACRatchetWeapons
from ..options import Missions
from .rule_helpers import HasGadget

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_high_rollers_casino_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    world.set_rule(mw.get_location(SACRatchetWeapons.PORKBOMB, player), True_())
    world.set_rule(mw.get_location(SACRatchetWeapons.HYPNOWATCH, player), True_())
    world.set_rule(mw.get_location(SACRatchetWeapons.HOLOMONOCLE, player), True_())
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.HIGH_ROLLERS_CASINO_1, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.HIGH_ROLLERS_CASINO_EXPLORE_PARADISE, player), True_())
        world.set_rule(mw.get_location(SACMissionLocations.HIGH_ROLLERS_CASINO_PARADISE_EXPLOITED, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.HIGH_ROLLERS_CASINO_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.HIGH_ROLLERS_CASINO_ENTER_CUTSCENE, player), True_())
        world.set_rule(mw.get_location(SACCutsceneLocations.HIGH_ROLLERS_CASINO_COMPLETE_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.HIGH_ROLLERS_CASINO_BEAT_THE_HOUSE, player), True_())

    # Alien code (AllAlienCodes) -- also needs Therm-Optic Shades
    if world.options.all_alien_codes:
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_COLINS_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_SHANES_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )
        world.set_rule(
            mw.get_location(SACAlienCodeLocations.HIGH_ROLLERS_CASINO_THE_PING_PONG_SECRET, player),
            HasGadget(THERM_OPTIC_SHADES),
        )

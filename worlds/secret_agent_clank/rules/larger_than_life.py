"""Larger Than Life's per-location rules -- every location belonging to
this case is set here explicitly (mirrors worlds/rac_size_matters/rules'
per-planet files, one world.set_rule() call per location, grouped by
which options.py toggle gates that location's category -- a location
only exists in the multiworld at all when its category's option is on,
so calling get_location() on it unguarded would raise). Reaching the
case at all is already gated by its "To Larger Than Life" entrance (see
rules/entrances.py's set_entrance_rules()), so most locations just need
True_() here; alien code locations additionally need Therm-Optic Shades
on top."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.cutscenes import SACCutsceneLocations
from ..constants.missions import SACMissionLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..options import Missions

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_larger_than_life_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.LARGER_THAN_LIFE_QWARKOGRAPHY_CH_1, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.LARGER_THAN_LIFE_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.LARGER_THAN_LIFE_ENTER_CUTSCENE, player), True_())
        world.set_rule(mw.get_location(SACCutsceneLocations.LARGER_THAN_LIFE_GODZILLA_LAZER_BEAM, player), True_())
        world.set_rule(mw.get_location(SACCutsceneLocations.LARGER_THAN_LIFE_COMPLETE_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.LARGER_THAN_LIFE_INVERSE_NINJA_LAW, player), True_())
        world.set_rule(mw.get_location(SACSkillPointLocations.LARGER_THAN_LIFE_BLASTER_OVERLOAD, player), True_())

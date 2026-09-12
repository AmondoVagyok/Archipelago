"""The Mess Hall's per-location rules -- every location belonging to
this case is set here explicitly (mirrors worlds/rac_size_matters/rules'
per-planet files, one world.set_rule() call per location, grouped by
which options.py toggle gates that location's category -- a location
only exists in the multiworld at all when its category's option is on,
so calling get_location() on it unguarded would raise). Reaching the
case at all is already gated by its "To The Mess Hall" entrance (see
rules/entrances.py's set_entrance_rules()), so most locations just need
True_() here; alien code locations additionally need Therm-Optic Shades
on top."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.cutscenes import SACCutsceneLocations
from ..constants.missions import SACMissionLocations
from ..constants.ratchet_challenges import SACRatchetChallengeLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..constants.titanium_bolts import SACTitaniumBoltLocations
from ..options import Missions

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_the_mess_hall_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    world.set_rule(mw.get_location(SACRatchetChallengeLocations.THE_MESS_HALL_NAILS_FOR_BREAKFAST, player), True_())
    world.set_rule(mw.get_location(SACRatchetChallengeLocations.THE_MESS_HALL_TYHRRANOID_RECYCLING, player), True_())
    world.set_rule(
        mw.get_location(SACRatchetChallengeLocations.THE_MESS_HALL_ITS_RAINING_PHLEGM_HALLELUJAH, player), True_(),
    )
    world.set_rule(mw.get_location(SACRatchetChallengeLocations.THE_MESS_HALL_MEATLOAF_TUESDAYS, player), True_())
    world.set_rule(
        mw.get_location(SACRatchetChallengeLocations.THE_MESS_HALL_MEGA_CHALLENGE_CAFETERIA, player), True_(),
    )
    world.set_rule(mw.get_location(SACTitaniumBoltLocations.THE_MESS_HALL_1, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.THE_MESS_HALL_NO_TIME_FOR_SECONDS, player), True_())
        world.set_rule(mw.get_location(SACMissionLocations.THE_MESS_HALL_THE_LUNCH_MENU_FOREVER, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.THE_MESS_HALL_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.THE_MESS_HALL_ENTER_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.THE_MESS_HALL_EMPTY_THE_WARRENS, player), True_())
        world.set_rule(mw.get_location(SACSkillPointLocations.THE_MESS_HALL_ANTAEUS, player), True_())

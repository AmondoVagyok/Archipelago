"""Inside the A-Eye's per-location rules -- every location belonging to
this case is set here explicitly (mirrors worlds/rac_size_matters/rules'
per-planet files, one world.set_rule() call per location, grouped by
which options.py toggle gates that location's category -- a location
only exists in the multiworld at all when its category's option is on,
so calling get_location() on it unguarded would raise). Reaching the
case at all is already gated by its "To Inside the A-Eye" entrance (see
rules/entrances.py's set_entrance_rules()), so most locations just need
True_() here; alien code locations additionally need Therm-Optic Shades
on top."""
from typing import TYPE_CHECKING

from rule_builder.rules import True_

from ..constants.cutscenes import SACCutsceneLocations
from ..constants.gadgetbot_challenges import SACGadgetbotChallengeLocations
from ..constants.missions import SACMissionLocations
from ..constants.skillpoints import SACSkillPointLocations
from ..constants.clank_gadgets import SACClankGadgets
from ..constants.weapons import SACRatchetWeapons
from ..options import Missions

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_inside_the_a_eye_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld

    # Always-on
    # SHOCKROCKET/BOLTGRABBER's only native source is the vendor (see
    # core/patches/locations.py's VENDOR_LOCATIONS) -- regions.py excludes
    # them from generation entirely when Clank is disabled (no vendor
    # exists at all), even though this case's own operative is Gadgetbots.
    if world.has_vendor:
        world.set_rule(mw.get_location(SACRatchetWeapons.SHOCKROCKET, player), True_())
        world.set_rule(mw.get_location(SACClankGadgets.BOLTGRABBER, player), True_())
    world.set_rule(mw.get_location(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_VAULTBREAKERS, player), True_())
    world.set_rule(mw.get_location(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_DARK_HELMET, player), True_())
    world.set_rule(mw.get_location(SACGadgetbotChallengeLocations.INSIDE_THE_A_EYE_GO_LONG, player), True_())

    # Story mission (Missions)
    if world.options.all_missions.value == Missions.option_all:
        world.set_rule(mw.get_location(SACMissionLocations.INSIDE_THE_A_EYE_PAYBACK_S_A_PUNCH, player), True_())
        world.set_rule(mw.get_location(SACMissionLocations.INSIDE_THE_A_EYE_MYE_MYNDE_IS_GOING, player), True_())
    else:
        world.set_rule(mw.get_location(SACMissionLocations.INSIDE_THE_A_EYE_COMPLETE, player), True_())

    # Cutscene (AllCutscenes)
    if world.options.all_cutscenes:
        world.set_rule(mw.get_location(SACCutsceneLocations.INSIDE_THE_A_EYE_COMPLETE_CUTSCENE, player), True_())

    # Skill point (SkillPoints)
    if world.options.skill_points:
        world.set_rule(mw.get_location(SACSkillPointLocations.INSIDE_THE_A_EYE_DIA_DE_LOS_MUERTOS, player), True_())

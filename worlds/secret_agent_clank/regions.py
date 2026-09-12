"""Regions are one per CASE now (not per Operative -- see git history for
the old grouping), each connected from Menu by a "To <Case>" entrance
whose rule is that case's access gate. This module doesn't set that
gate itself -- entrance rules are set by rules/entrances.py's
set_entrance_rules() (mirroring worlds/rac_size_matters/rules/
entrances.py's per-planet pattern), run later during set_rules() (see
rules/__init__.py's docstring), and any real per-location extra
requirement (e.g. alien codes needing Therm-Optic Shades) lives in
rules/<case>.py alongside it -- see that module for why locations don't
need their own case-access rule anymore now that the entrance gates it.
The one exception is _create_victory() below: it still sets its own
Victory event locations' rule directly with rule_helpers.py's
case_access_rule() (the same rule set_entrance_rules() puts on the
matching entrances), since those locations are also created here and
there's nowhere else in the flow that currently touches them.

An operative disabled via options.py's Operatives option has ALL of their
cases' regions/locations excluded from generation entirely here, rather
than left in place behind a permanently-false rule -- a permanently
unreachable location with a real item requirement placed there would
either break fill or waste a progression item slot; skipping creation
avoids that outright (matches the user's "their missions will not
unlock" -- the content doesn't exist in this seed, not just "you can't
reach it"). Special Missions is a real, independently toggleable operative
here same as the four playable characters (see constants/operatives.py's
module docstring)."""
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import CanReachLocation, CanReachRegion, Has, True_

from Options import OptionError

from .constants import (
    ALIEN_CODES,
    ALL_CASES,
    CASES_BY_OPERATIVE,
    GOAL_CASE,
    KEYCARDS,
    SACOperatives,
)
from .entities import SACLocation
from .locations import (
    ALIEN_CODE_LOCATIONS,
    ALL_STORY_MISSION_LOCATIONS,
    ALWAYS_ON_LOCATIONS,
    CUTSCENE_LOCATIONS,
    KEYCARD_LOCATIONS,
    SKILL_POINT_LOCATIONS,
    STORY_MISSION_LOCATIONS,
)
from .options import Goal, Missions
from .rules.rule_helpers import case_access_rule, disabled_operatives

if TYPE_CHECKING:
    from .world import SecretAgentClankWorld


def create_regions(world: "SecretAgentClankWorld") -> None:
    player = world.player
    multiworld = world.multiworld
    disabled = disabled_operatives(world)

    menu_region = Region("Menu", player, multiworld)
    from .constants.weapon_mods import enabled_mods
    from .locations import MOD_VENDOR_LOCATIONS
    from .rules.vendor_access import VENDOR_REQUIREMENTS
    from rule_builder.rules import False_
    # The vendor is only ever reachable from Clank's pause-menu screen (see
    # rules/vendor_access.py's VENDOR_REQUIREMENTS) -- Clank disabled means
    # no vendor at all, regardless of what any individual case's entry says.
    has_vendor = SACOperatives.CLANK not in disabled and any(
        case.operative not in disabled and
        not isinstance(VENDOR_REQUIREMENTS.get(case.name, False_()), False_)
        for case in ALL_CASES
    )
    world.has_vendor = has_vendor
    world.weapon_mod_catalog = (
        enabled_mods(world.options.operatives.value, world.options.ng_plus.value) if has_vendor else ()
    )
    # Weapons/gadgets whose ONLY native source is the vendor (see
    # core/location_hooks.py's VENDOR_LOCATIONS, applied by
    # rules/vendor_access.py's set_vendor_rules()) can never be obtained at
    # all once Clank is disabled -- exclude them from generation outright
    # (same principle as the module docstring's disabled-operative case
    # exclusion) instead of leaving a location no item can ever fill.
    vendor_only_names: frozenset[str] = frozenset()
    if not has_vendor:
        from .rules.vendor_access import VENDOR_ONLY_ITEM_NAMES
        vendor_only_names = VENDOR_ONLY_ITEM_NAMES
    if world.using_ut:
        saved_ids = world.passthrough.get('weapon_mod_ids', ())
        world.weapon_mod_catalog = tuple(mod for mod in enabled_mods(
            world.options.operatives.value, world.options.ng_plus.value) if mod.mod_id in saved_ids)
    if world.weapon_mod_catalog:
        mod_region = Region('Mod Vendor', player, multiworld)
        for mod in world.weapon_mod_catalog:
            mod_region.locations.append(SACLocation(player, mod.location,
                MOD_VENDOR_LOCATIONS[mod.location].code, mod_region))
        menu_region.connect(mod_region)
        multiworld.regions.append(mod_region)
    if world.options.ng_plus.value and has_vendor:
        from .locations import TITAN_VENDOR_LOCATIONS
        vendor_region = Region('Titan Vendor', player, multiworld)
        for name, data in TITAN_VENDOR_LOCATIONS.items():
            vendor_region.locations.append(SACLocation(player, name, data.code, vendor_region))
        menu_region.connect(vendor_region)
        multiworld.regions.append(vendor_region)
    case_regions: dict[str, Region] = {
        case.name: Region(case.name, player, multiworld)
        for case in ALL_CASES if case.operative not in disabled
    }

    location_tables = [ALWAYS_ON_LOCATIONS]
    # Missions: exactly one of these two sets is used per seed, never both
    # -- level_completion is one location per case ("{Case} Complete"),
    # all is one location per individual CHAPTER_ENTRIES mission within
    # each case (see locations/__init__.py's docstring and each case
    # file's own *_MISSION_LOCATIONS / *_ALL_MISSIONS_LOCATIONS dicts).
    if world.options.all_missions.value == Missions.option_all:
        location_tables.append(ALL_STORY_MISSION_LOCATIONS)
    else:
        location_tables.append(STORY_MISSION_LOCATIONS)
    if world.options.skill_points:
        location_tables.append(SKILL_POINT_LOCATIONS)
    if world.options.all_cutscenes:
        location_tables.append(CUTSCENE_LOCATIONS)
    if world.options.all_keycards:
        location_tables.append(KEYCARD_LOCATIONS)

    for table in location_tables:
        for loc_name, loc_data in table.items():
            if loc_name in vendor_only_names:
                continue
            region = case_regions.get(loc_data.case)
            if region is None:
                continue
            location = SACLocation(player, loc_name, loc_data.code, region)
            region.locations.append(location)

    # Alien Codes -- only the case-confirmed codes exist here at all
    # (ALIEN_CODE_LOCATIONS already excludes the still-TODO ones). Gated
    # on its own option (not just folded into location_tables above) to
    # match create_regions()'s own per-category option checks.
    if world.options.all_alien_codes:
        for loc_name, loc_data in ALIEN_CODE_LOCATIONS.items():
            region = case_regions.get(loc_data.case)
            if region is None:
                continue
            location = SACLocation(player, loc_name, loc_data.code, region)
            region.locations.append(location)

    _create_victory(world, case_regions, disabled)

    for case_name, region in case_regions.items():
        menu_region.connect(region, f"To {case_name}")

    multiworld.regions += [menu_region, *case_regions.values()]


def _create_victory(
    world: "SecretAgentClankWorld", case_regions: dict[str, Region], disabled_operatives: set[str],
) -> None:
    """Places a locked "Victory" event per active goal condition (see
    options.py's Goal) -- reaching ANY of them satisfies
    multiworld.completion_condition (see rules.py's set_rules()), so
    Goal=any naturally becomes an OR by placing both.

    Raises OptionError instead of generating an unbeatable seed if the
    selected goal's required character(s) are disabled via the Operatives
    option (Defeat Klunk needs Clank; Qwark Opera needs Qwark; All Gadgetbots
    needs Gadgetbots; Ratchet Prison Escape needs Ratchet; Any needs at
    least one of Clank/Qwark)."""
    player = world.player
    player_name = world.multiworld.get_player_name(player)
    goal = world.options.goal.value
    clank_disabled = SACOperatives.CLANK in disabled_operatives
    qwark_disabled = SACOperatives.QWARK in disabled_operatives
    gadgetbots_disabled = SACOperatives.GADGETBOTS in disabled_operatives
    ratchet_disabled = SACOperatives.RATCHET in disabled_operatives

    if goal == Goal.option_defeat_klunk and clank_disabled:
        raise OptionError(
            f"{player_name}'s Secret Agent Clank: Goal is Defeat Klunk, which requires Clank, "
            "but Clank is disabled via the Operatives option."
        )
    if goal == Goal.option_qwark_opera and qwark_disabled:
        raise OptionError(
            f"{player_name}'s Secret Agent Clank: Goal is Qwark Opera, which requires Qwark, "
            "but Qwark is disabled via the Operatives option."
        )
    if goal == Goal.option_any and clank_disabled and qwark_disabled:
        raise OptionError(
            f"{player_name}'s Secret Agent Clank: Goal is Any, which requires Clank or Qwark, "
            "but both are disabled via the Operatives option."
        )
    if goal == Goal.option_all_gadgetbots and gadgetbots_disabled:
        raise OptionError(
            f"{player_name}'s Secret Agent Clank: Goal is All Gadgetbots, which requires Gadgetbots, "
            "but Gadgetbots is disabled via the Operatives option."
        )
    if goal == Goal.option_ratchet_prison_escape and ratchet_disabled:
        raise OptionError(
            f"{player_name}'s Secret Agent Clank: Goal is Ratchet Prison Escape, which requires Ratchet, "
            "but Ratchet is disabled via the Operatives option."
        )

    def add_victory(name: str, region: Region, rule) -> None:
        loc = SACLocation(player, name, None, region)
        loc.place_locked_item(world.create_event("Victory"))
        world.set_rule(loc, rule)
        region.locations.append(loc)

    if goal in (Goal.option_alien_codes, Goal.option_chalice_of_power):
        entries = ALIEN_CODES if goal == Goal.option_alien_codes else KEYCARDS
        rule = True_()
        for entry in entries:
            if entry.case_name not in case_regions:
                raise OptionError(f'{player_name}: the selected goal requires disabled case {entry.case_name}.')
            locations_enabled = (world.options.all_alien_codes if goal == Goal.option_alien_codes
                                 else world.options.all_keycards)
            if locations_enabled:
                rule = rule & CanReachLocation(str(entry))
            else:
                # Native collectibles remain available without AP reward checks.
                rule = rule & CanReachRegion(entry.case_name)
        if goal == Goal.option_alien_codes:
            from .constants.clank_gadgets import THERM_OPTIC_SHADES
            rule = rule & Has(THERM_OPTIC_SHADES)
        title = 'All Alien Codes' if goal == Goal.option_alien_codes else 'Collect the Chalice of Power'
        add_victory(f'Victory: {title}', case_regions[entries[0].case_name], rule)

    if goal in (Goal.option_defeat_klunk, Goal.option_any) and not clank_disabled:
        case = GOAL_CASE
        add_victory("Victory: Defeat Klunk", case_regions[case.name], case_access_rule(world, case))

    if goal in (Goal.option_qwark_opera, Goal.option_any) and not qwark_disabled:
        qwark_cases = CASES_BY_OPERATIVE[SACOperatives.QWARK]
        rule = case_access_rule(world, qwark_cases[0])
        for case in qwark_cases[1:]:
            rule = rule & case_access_rule(world, case)
        add_victory("Victory: Qwark Opera", case_regions[qwark_cases[0].name], rule)

    if goal == Goal.option_all_gadgetbots and not gadgetbots_disabled:
        gadgetbot_cases = CASES_BY_OPERATIVE[SACOperatives.GADGETBOTS]
        rule = case_access_rule(world, gadgetbot_cases[0])
        for case in gadgetbot_cases[1:]:
            rule = rule & case_access_rule(world, case)
        add_victory("Victory: All Gadgetbots", case_regions[gadgetbot_cases[0].name], rule)

    if goal == Goal.option_ratchet_prison_escape and not ratchet_disabled:
        from .constants.ratchet_challenges import RATCHET_CHALLENGES
        rule = True_()
        for entry in RATCHET_CHALLENGES:
            rule = rule & CanReachLocation(str(entry))
        add_victory(
            "Victory: Ratchet Prison Escape", case_regions[RATCHET_CHALLENGES[0].case_name], rule,
        )

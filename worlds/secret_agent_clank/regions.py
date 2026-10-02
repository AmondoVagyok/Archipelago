"""One region per case, each entered from Menu through a "To <Case>" entrance gated by that case's access rule."""
from typing import TYPE_CHECKING

from BaseClasses import Region
from Options import OptionError
from rule_builder.rules import CanReachLocation, CanReachRegion, False_, Has, True_

from .constants import (
    ALIEN_CODES,
    ALL_CASES,
    CASE_NAME_TO_CASE,
    CASES_BY_OPERATIVE,
    KEYCARDS,
    SACCases,
    SACOperatives,
)
from .constants.clank_gadgets import SACClankGadgets
from .constants.ratchet_challenges import RATCHET_CHALLENGES
from .constants.weapon_mods import enabled_mods
from .constants.weapon_progression import TITAN_LOCATIONS
from .constants.weapons import EQUIPMENT_INTERNAL_TO_DISPLAY
from .entities import SACLocation
from .locations import BASE_VENDOR_LOCATIONS, CASE_LOCATIONS, MOD_VENDOR_LOCATIONS, TITAN_VENDOR_LOCATIONS
from .locations.nanotech import create_nanotech_locations
from .locations.stealth import create_stealth_locations
from .locations.weapon_levels import create_weapon_level_locations
from .options import Goal
from .rules.rule_helpers import case_access_rule, disabled_operatives
from .rules.vendor_access import VENDOR_REQUIREMENTS

if TYPE_CHECKING:
    from .world import SecretAgentClankWorld

# Stable sort: within a case region, locations keep their case file's order per type.
REGION_LOCATIONS = tuple(sorted(CASE_LOCATIONS, key=lambda location: location.region_order))


def create_regions(world: "SecretAgentClankWorld") -> None:
    player = world.player
    multiworld = world.multiworld
    disabled = disabled_operatives(world)

    menu_region = Region("Menu", player, multiworld)
    # The vendor is opened from Clank's pause menu, so it needs Clank and at least
    # one enabled case with a vendor route.
    has_vendor = SACOperatives.CLANK not in disabled and any(
        case.operative not in disabled and
        not isinstance(VENDOR_REQUIREMENTS.get(case.name, False_()), False_)
        for case in ALL_CASES
    )
    world.has_vendor = has_vendor
    world.weapon_mod_catalog = (
        enabled_mods(world.options.operatives.value, world.options.ng_plus.value) if has_vendor else ()
    )
    if world.using_ut:
        saved_ids = world.passthrough.get("weapon_mod_ids", ())
        world.weapon_mod_catalog = tuple(mod for mod in enabled_mods(
            world.options.operatives.value, world.options.ng_plus.value) if mod.mod_id in saved_ids)
    if has_vendor:
        vendor_region = Region("Vendor", player, multiworld)
        def enabled_item(name):
            return (SACOperatives.CLANK if name.endswith("(Clank)")
                    else SACOperatives.RATCHET) not in disabled
        for definition in BASE_VENDOR_LOCATIONS.values():
            if enabled_item(definition.name) and definition.available(world.options):
                vendor_region.locations.append(SACLocation(
                    player, definition.name, definition.code, vendor_region))
        for mod in world.weapon_mod_catalog:
            vendor_region.locations.append(SACLocation(
                player, mod.location, MOD_VENDOR_LOCATIONS[mod.location].code, vendor_region))
        if world.options.ng_plus.value:
            for internal, name in TITAN_LOCATIONS.items():
                if enabled_item(EQUIPMENT_INTERNAL_TO_DISPLAY[internal]):
                    vendor_region.locations.append(SACLocation(
                        player, name, TITAN_VENDOR_LOCATIONS[name].code, vendor_region))
        menu_region.connect(vendor_region)
        multiworld.regions.append(vendor_region)
    case_regions: dict[str, Region] = {
        case.name: Region(case.name, player, multiworld)
        for case in ALL_CASES if case.operative not in disabled
    }

    for definition in REGION_LOCATIONS:
        if not definition.available(world.options):
            continue
        region = case_regions.get(definition.case)
        if region is None:
            continue
        region.locations.append(SACLocation(player, definition.name, definition.code, region))

    _create_victory(world, case_regions, disabled)

    for case_name, region in case_regions.items():
        menu_region.connect(region, f"To {case_name}")

    multiworld.regions += [menu_region, *case_regions.values()]
    create_weapon_level_locations(world, menu_region)
    create_nanotech_locations(world, menu_region)
    create_stealth_locations(world, menu_region)


def _create_victory(
    world: "SecretAgentClankWorld", case_regions: dict[str, Region], disabled_operatives: set[str],
) -> None:
    """Place a locked Victory event for each condition of the chosen goal; reaching any one completes the game."""
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
                raise OptionError(f"{player_name}: the selected goal requires disabled case {entry.case_name}.")
            locations_enabled = (world.options.all_alien_codes if goal == Goal.option_alien_codes
                                 else world.options.all_keycards)
            if locations_enabled:
                rule = rule & CanReachLocation(str(entry))
            else:
                # Native collectibles remain available without AP reward checks.
                rule = rule & CanReachRegion(entry.case_name)
        if goal == Goal.option_alien_codes:
            rule = rule & Has(SACClankGadgets.THERM_OPTIC_SHADES)
        title = "All Alien Codes" if goal == Goal.option_alien_codes else "Collect the Chalice of Power"
        add_victory(f"Victory: {title}", case_regions[entries[0].case_name], rule)

    if goal in (Goal.option_defeat_klunk, Goal.option_any) and not clank_disabled:
        case = CASE_NAME_TO_CASE[SACCases.KLUNKS_LAIR]
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
        rule = True_()
        for entry in RATCHET_CHALLENGES:
            rule = rule & CanReachLocation(str(entry))
        add_victory(
            "Victory: Ratchet Prison Escape", case_regions[RATCHET_CHALLENGES[0].case_name], rule,
        )

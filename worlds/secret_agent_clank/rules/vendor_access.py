from rule_builder.rules import CanReachRegion, False_, Has, True_

from ..constants.challenge_mode import CHALLENGE_VENDOR_LOCATIONS, PROGRESSIVE_CHALLENGE_MODE
from ..constants.clank_gadgets import SACClankGadgets
from ..constants.planets import SACCases, CASE_NAME_TO_CASE, CASES_BY_OPERATIVE, PLANET_ACCESS_ITEM_NAME
from ..constants import CHARACTER_ITEM_NAME, PROGRESSIVE_CHARACTER_ITEM_NAME
from ..items import PROGRESSIVE_PLANET_ITEM_NAME
from ..options import Infobots
from ..constants.vendor_unlocks import VENDOR_CASES
from ..constants.weapons import EQUIPMENT_DISPLAY_TO_INTERNAL
from ..core.patches import VENDOR_LOCATIONS

VENDOR_ONLY_ITEM_NAMES: frozenset[str] = frozenset(
    name for name, internal in EQUIPMENT_DISPLAY_TO_INTERNAL.items()
    if internal in VENDOR_LOCATIONS.values()
)

# Fill in the physical vendor routes here; no extra item gates are guessed.
VENDOR_REQUIREMENTS = {
    SACCases.BOLTAIRE_MUSEUM: Has(SACClankGadgets.BLACK_OUT_PEN),
    SACCases.BOLTAIRE_GEM_WING: False_(),
    SACCases.MAX_SECURITY_CELLS: False_(),
    SACCases.ROOFTOP_DEATHTRAP: False_(),
    SACCases.ASYANICA_ROOFTOPS: True_(),
    SACCases.LARGER_THAN_LIFE: False_(),
    SACCases.COUNTESS_VILLA: False_(), # this is disabled until rules are fully sorted for planets it is possible to access if special missions are enabled
    SACCases.GLACIARA_SKI_SLOPES: False_(),
    SACCases.THE_MESS_HALL: False_(),
    SACCases.AZCOTAL_ALLEY: True_(),
    SACCases.GONDOLA_ASCENT: True_(),
    SACCases.SUCK_AND_JIVE: False_(),
    SACCases.HIGH_ROLLERS_CASINO: False_(),
    SACCases.THE_EXERCISE_YARD: False_(),
    SACCases.HIGH_STAKES_ROOM: False_(),
    SACCases.VENANTONIO_LABS: True_(),
    SACCases.VENANTONIO_CANALS: False_(),
    SACCases.MADAM_BUTTERQWARK: False_(),
    SACCases.GALACTIC_BOLT_RESERVE: True_(),
    SACCases.INSIDE_THE_A_EYE: False_(),
    SACCases.THE_SHOWERS: False_(),
    SACCases.SPACESHIP_GRAVEYARD: True_(),
    SACCases.SAINT_QWARK: False_(),
    SACCases.THE_QUASAR_FIELDS: False_(),
    SACCases.PRISON_BREAKOUT: False_(),
    SACCases.DAMS_EDGE_HYDRANO: False_(),
    SACCases.A_FICTION_FULL_OF_DOLLARS: False_(),
    SACCases.BULKHEAD_LOCK: False_(),
    SACCases.UNDERWATER_BUNKER: True_(),
    SACCases.KLUNKS_LAIR: True_(),
    SACCases.HIGH_TREEHOUSE: False_(),
}


def vendor_access_rule(world, case_name):
    existing = {r.name for r in world.multiworld.get_regions(world.player)}
    if case_name not in existing:
        return False_()
    return CanReachRegion(case_name) & VENDOR_REQUIREMENTS.get(case_name, False_())


def any_vendor_rule(world):
    rule = False_()
    for case_name in VENDOR_REQUIREMENTS:
        rule = rule | vendor_access_rule(world, case_name)
    return rule


def vendor_case_rule(world, case_name):
    """Match resolved AP case ownership, including alternative access modes."""
    rule = Has(case_name)
    case = CASE_NAME_TO_CASE[case_name]
    mode = world.options.infobots
    if mode == Infobots.option_character_unlocks:
        item = PROGRESSIVE_CHARACTER_ITEM_NAME.get(case.operative)
        if item:
            count = list(CASES_BY_OPERATIVE[case.operative]).index(case) + 1
            return rule | Has(item, count)
        return rule | Has(CHARACTER_ITEM_NAME[case.operative])
    if mode == Infobots.option_progressive_planet:
        if case.planet in world.progressive_planets:
            return rule | Has(PROGRESSIVE_PLANET_ITEM_NAME,
                              world.progressive_planets.index(case.planet) + 1)
    elif mode != Infobots.option_cases and case.planet in PLANET_ACCESS_ITEM_NAME:
        return rule | Has(PLANET_ACCESS_ITEM_NAME[case.planet])
    return rule


def set_vendor_rules(world):
    # Unlock the slot with its case, independently of the randomized reward.
    available_vendor = any_vendor_rule(world)
    for location in world.multiworld.get_locations(world.player):
        if location.parent_region.name == "Vendor":
            rule = available_vendor & vendor_case_rule(world, VENDOR_CASES[location.name])
            if world.options.progressive_challenge_mode and location.name in CHALLENGE_VENDOR_LOCATIONS:
                rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
            world.set_rule(location, rule)

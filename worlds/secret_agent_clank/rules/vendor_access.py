from rule_builder.rules import CanReachRegion, False_, Has, True_

from ..constants.clank_gadgets import SACClankGadgets
from ..constants.planets import SACCases
from ..constants.weapons import (
    GADGET_DISPLAY_TO_INTERNAL,
    RATCHET_WEAPON_DISPLAY_TO_INTERNAL,
)
from ..core.patches import VENDOR_LOCATIONS

VENDOR_ONLY_ITEM_NAMES: frozenset[str] = frozenset(
    name for name, internal in {**RATCHET_WEAPON_DISPLAY_TO_INTERNAL, **GADGET_DISPLAY_TO_INTERNAL}.items()
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


def set_vendor_rules(world):
    # Every purchase uses the same physical vendor access. Native inventory,
    # original pickup cases and weapon levels do not gate AP purchase checks.
    available_vendor = any_vendor_rule(world)
    for location in world.multiworld.get_locations(world.player):
        if location.parent_region.name == "Vendor":
            world.set_rule(location, available_vendor)

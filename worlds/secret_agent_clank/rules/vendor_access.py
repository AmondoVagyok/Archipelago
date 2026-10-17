from dataclasses import dataclass

from rule_builder.rules import CanReachRegion, False_, Has, HasAll, Rule, TWorld
from typing_extensions import override

from ..constants import (
    ALL_CASES,
    CASES_BY_OPERATIVE,
    CASE_NAME_TO_CASE,
    EQUIPMENT_DISPLAY_TO_INTERNAL,
    PLANET_ACCESS_ITEM_NAME,
    PROGRESSIVE_CHARACTER_ITEM_NAME,
    VENDOR_REQUIREMENT_ITEMS,
)
from ..constants import VENDOR_LOCATIONS
from ..options import Infobots
from .rule_helpers import HasProgressivePlanet, region_names

VENDOR_ONLY_ITEM_NAMES: frozenset[str] = frozenset(
    name for name, internal in EQUIPMENT_DISPLAY_TO_INTERNAL.items()
    if internal in VENDOR_LOCATIONS.values()
)

VENDOR_REQUIREMENTS = {
    case.name: HasAll(*VENDOR_REQUIREMENT_ITEMS[case.name]) if case.name in VENDOR_REQUIREMENT_ITEMS else False_()
    for case in ALL_CASES
}


@dataclass
class CaseOwnershipRule(Rule[TWorld], game="Secret Agent Clank"):
    """Match resolved AP case ownership, including alternative access modes."""

    cases: str

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = Has(self.cases)
        case = CASE_NAME_TO_CASE[self.cases]
        mode = world.options.infobots
        if mode == Infobots.option_character_unlocks:
            item = PROGRESSIVE_CHARACTER_ITEM_NAME.get(case.operative)
            if item:
                rule = rule | Has(item, list(CASES_BY_OPERATIVE[case.operative]).index(case) + 1)
        elif mode == Infobots.option_progressive_planet:
            rule = rule | HasProgressivePlanet(world, self.cases)
        elif mode != Infobots.option_cases and case.planet in PLANET_ACCESS_ITEM_NAME:
            rule = rule | Has(PLANET_ACCESS_ITEM_NAME[case.planet])
        return rule.resolve(world)


@dataclass
class VendorCaseRule(Rule[TWorld], game="Secret Agent Clank"):
    cases: str

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if self.cases not in region_names(world):
            return False_().resolve(world)
        rule = CanReachRegion(self.cases) & VENDOR_REQUIREMENTS.get(self.cases, False_())
        return (rule & CaseOwnershipRule(self.cases)).resolve(world)


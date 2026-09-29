"""Editable access rules for the three cumulative stealth milestone tiers."""
from rule_builder.rules import CanReachRegion, False_, True_
from ..constants import CASES_BY_OPERATIVE, SACOperatives


def _all_clank_cases(world):
    """Conservative fallback until the actual takedown routes are mapped."""
    existing = {region.name for region in world.multiworld.get_regions(world.player)}
    cases = [case.name for case in CASES_BY_OPERATIVE[SACOperatives.CLANK] if case.name in existing]
    if not cases:
        return False_()
    rule = True_()
    for case in cases:
        rule = rule & CanReachRegion(case)
    return rule


def stealth_5_rule(world):
    # TODO: Replace with cases/items that allow 5 successful stealth takedowns.
    return _all_clank_cases(world)


def stealth_10_rule(world):
    # TODO: Replace with cases/items that allow 10 cumulative stealth takedowns.
    return _all_clank_cases(world)


def stealth_25_rule(world):
    # TODO: Replace with cases/items that allow 25 cumulative stealth takedowns.
    return _all_clank_cases(world)


def stealth_access_rule(world, count):
    if not 1 <= count <= 25:
        raise ValueError("Stealth milestone must be between 1 and 25")
    rule = stealth_5_rule(world)
    if count > 5:
        rule = rule & stealth_10_rule(world)
    if count > 10:
        rule = rule & stealth_25_rule(world)
    return rule

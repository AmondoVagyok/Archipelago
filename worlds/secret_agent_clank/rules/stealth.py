"""Editable access rules for the three cumulative stealth milestone tiers."""
from ..constants import CASES_BY_OPERATIVE, SACOperatives
from .rule_helpers import can_reach_all_cases


def _all_clank_cases(world):
    """Conservative fallback until the actual takedown routes are mapped."""
    return can_reach_all_cases(world, (case.name for case in CASES_BY_OPERATIVE[SACOperatives.CLANK]))


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

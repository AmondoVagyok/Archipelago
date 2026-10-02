"""Editable access rules for Clank Nanotech level checks, tiered by Clank cases reached."""
from typing import TYPE_CHECKING

from rule_builder.rules import CanReachRegion, False_, Has, Rule, True_
from ..constants import CASES_BY_OPERATIVE, SACOperatives
from ..constants.challenge_mode import PROGRESSIVE_CHALLENGE_MODE
from ..constants.nanotech import CLANK_NG_CAP
from .rule_helpers import HasEnemyAccess

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld

NANOTECH_EARLY_CAP = 30
"""Levels up to this need one Clank case with enemies; above it (incl. NG+) need every Clank case."""


def _existing_cases(world: "SecretAgentClankWorld", cases) -> list[str]:
    existing = {region.name for region in world.multiworld.get_regions(world.player)}
    return [case for case in cases if case in existing]


def _all_cases(cases: list[str]) -> Rule:
    if not cases:
        return False_()
    rule = True_()
    for case in cases:
        rule = rule & CanReachRegion(case)
    return rule


def nanotech_late_rule(world: "SecretAgentClankWorld") -> Rule:
    return _all_cases(_existing_cases(world, (case.name for case in CASES_BY_OPERATIVE[SACOperatives.CLANK])))


def nanotech_access_rule(world: "SecretAgentClankWorld", level: int) -> Rule:
    if level <= NANOTECH_EARLY_CAP:
        return HasEnemyAccess(world)
    rule = nanotech_late_rule(world)
    if world.options.progressive_challenge_mode and level > CLANK_NG_CAP:
        rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
    return rule

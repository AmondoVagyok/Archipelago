from dataclasses import dataclass

from rule_builder.rules import CanReachRegion, False_, Has, Rule, TWorld
from typing_extensions import override

from ..constants import (
    CASES_BY_OPERATIVE,
    CLANK_NG_CAP,
    CLANK_START_NANOTECH,
    PROGRESSIVE_CHALLENGE_MODE,
    RATCHET_NG_CAP,
    RATCHET_START_NANOTECH,
    SACOperatives,
)
from .rule_helpers import AtLeast, HasEnemyAccess, region_names

NANOTECH_LEVELS_PER_CASE = 10
"""Each Clank case with reachable enemies puts this many more Clank Nanotech levels in logic."""

RATCHET_NANOTECH_LEVELS_PER_CASE = 15
"""Each reachable Ratchet case puts this many more Ratchet Nanotech levels in logic."""


def nanotech_cases_required(level: int) -> int:
    """Clank cases with enemy access needed for `level`: 16-25 need one, 26-35 two, and so on."""
    return -(-(level - CLANK_START_NANOTECH) // NANOTECH_LEVELS_PER_CASE)


def ratchet_nanotech_cases_required(level: int) -> int:
    """Ratchet cases needed for `level`: 21-35 need one, 36-50 two, and so on."""
    return -(-(level - RATCHET_START_NANOTECH) // RATCHET_NANOTECH_LEVELS_PER_CASE)


@dataclass
class ClankNanotechRule(Rule[TWorld], game="Secret Agent Clank"):
    level: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = HasEnemyAccess(nanotech_cases_required(self.level))
        if world.options.progressive_challenge_mode and self.level > CLANK_NG_CAP:
            rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
        return rule.resolve(world)


@dataclass
class RatchetNanotechRule(Rule[TWorld], game="Secret Agent Clank"):
    level: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        existing = region_names(world)
        cases = [CanReachRegion(case.name) for case in CASES_BY_OPERATIVE[SACOperatives.RATCHET]
                 if case.name in existing]
        rule = AtLeast(min(ratchet_nanotech_cases_required(self.level), len(cases)), *cases) if cases else False_()
        if world.options.progressive_challenge_mode and self.level > RATCHET_NG_CAP:
            rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
        return rule.resolve(world)

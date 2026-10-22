from dataclasses import dataclass

from rule_builder.rules import CanReachRegion, Has, HasAll, HasAny, Rule, TWorld
from typing_extensions import override

from ..constants import SACCases, SACClankGadgets, SACClankWeapons
from .rule_helpers import HasProjectileWeapon

STEALTH_CASE_RULES = {
    SACCases.ASYANICA_ROOFTOPS: HasAll(SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS, SACClankGadgets.OMNIKEY),
    SACCases.VENANTONIO_LABS: Has(SACClankWeapons.CUFFLINK) & HasAny(SACClankWeapons.FLAMETHROWERPEN,
                                                                      SACClankGadgets.OMNIKEY),
    SACCases.GALACTIC_BOLT_RESERVE: HasAll(SACClankWeapons.CUFFLINK, SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS),
    SACCases.SPACESHIP_GRAVEYARD: Has(SACClankGadgets.JETBOOTS) & HasProjectileWeapon(),
}


@dataclass
class StealthCaseRule(Rule[TWorld], game="Secret Agent Clank"):
    cases: str

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = CanReachRegion(self.cases)
        if self.cases in STEALTH_CASE_RULES:
            rule = rule & STEALTH_CASE_RULES[self.cases]
        return rule.resolve(world)

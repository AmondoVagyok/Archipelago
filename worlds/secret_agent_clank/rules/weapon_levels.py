from dataclasses import dataclass

from rule_builder.rules import CanReachRegion, False_, Has, Or, Rule, TWorld
from typing_extensions import override

from ..constants import (
    CASES_BY_OPERATIVE,
    EQUIPMENT_INTERNAL_TO_DISPLAY,
    PROGRESSIVE_CHALLENGE_MODE,
    UNLOCK_TO_PROGRESSIVE,
    SACOperatives,
)
from .rule_helpers import HasEnemyAccess, region_names

CLANK_WEAPON_LEVEL_CASES: dict[str, tuple[str, ...]] = {
    "throwTie": (),
    "CuffLink": (),
    "TangleVine": (),
    "HoloKnuckles": (),
    "FlamethrowerPen": (),
    "LightningUmbrella": (),
}


@dataclass
class WeaponLevelRule(Rule[TWorld], game="Secret Agent Clank"):
    weapon: str
    level: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        name = EQUIPMENT_INTERNAL_TO_DISPLAY[self.weapon]
        operative = SACOperatives.CLANK if name.endswith("(Clank)") else SACOperatives.RATCHET
        existing = region_names(world)
        cases = CLANK_WEAPON_LEVEL_CASES.get(self.weapon, ()) or tuple(
            case.name for case in CASES_BY_OPERATIVE[operative])
        reachable = [CanReachRegion(case) for case in cases if case in existing]
        rule = Or(*reachable) if reachable else False_()
        if operative == SACOperatives.CLANK:
            rule = rule & HasEnemyAccess()
        rule = rule & (Has(UNLOCK_TO_PROGRESSIVE[name], self.level)
                       if world.options.progressive_weapons else Has(name))
        if world.options.progressive_challenge_mode and self.level > 4:
            rule = rule & Has(PROGRESSIVE_CHALLENGE_MODE)
        return rule.resolve(world)

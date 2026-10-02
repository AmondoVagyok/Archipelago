"""Shared rule builders, returning rule_builder rule objects."""
from collections.abc import Iterable
from typing import TYPE_CHECKING

from rule_builder.rules import CanReachRegion, False_, Has, Rule, True_

from ..constants import (
    CASE_NAME_TO_INFOBOT,
    CHARACTER_ITEM_NAME,
    PLANET_ACCESS_ITEM_NAME,
    PROGRESSIVE_CHARACTER_ITEM_NAME,
)
from ..constants.clank_gadgets import SACClankGadgets, SACClankWeapons
from ..constants.operatives import ALL_OPERATIVES, SACOperatives
from ..constants.planets import CASES_BY_OPERATIVE, SACCases
from ..constants.weapon_progression import UNLOCK_TO_PROGRESSIVE
from ..items import PROGRESSIVE_PLANET_ITEM_NAME
from ..options import Infobots

if TYPE_CHECKING:
    from ..constants.planets import Case
    from ..world import SecretAgentClankWorld


def region_names(world: "SecretAgentClankWorld") -> set[str]:
    """Names of every region created so far for this world's player."""
    return {region.name for region in world.multiworld.get_regions(world.player)}


def can_reach_all_cases(world: "SecretAgentClankWorld", case_names: Iterable[str]) -> Rule:
    """Reach every listed case that exists in this world; never satisfiable when none of them exist."""
    existing = region_names(world)
    cases = [case for case in case_names if case in existing]
    if not cases:
        return False_()
    rule = True_()
    for case in cases:
        rule = rule & CanReachRegion(case)
    return rule


def HasPlanet(world: "SecretAgentClankWorld", planet: str) -> Has | True_:
    if world.options.infobots == Infobots.option_progressive_planet:
        planets = world.progressive_planets
        return Has(PROGRESSIVE_PLANET_ITEM_NAME, planets.index(planet) + 1) if planet in planets else True_()
    if world.options.infobots in (Infobots.option_cases, Infobots.option_character_unlocks):
        return True_()
    item = PLANET_ACCESS_ITEM_NAME.get(planet)
    return Has(item) if item else True_()


def HasCase(world: "SecretAgentClankWorld", case_name: str) -> Has | True_:
    if world.options.infobots != Infobots.option_cases:
        return True_()
    item = CASE_NAME_TO_INFOBOT.get(case_name)
    return Has(item) if item else True_()


# Clank case -> items needed (on top of reaching the case) to get at its enemies.
CLANK_ENEMY_CASES: dict[str, tuple[str, ...]] = {
    SACCases.BOLTAIRE_MUSEUM:       (),
    SACCases.ASYANICA_ROOFTOPS:     (SACClankWeapons.THROWTIE,),
    SACCases.AZCOTAL_ALLEY:         (),
    SACCases.GONDOLA_ASCENT:        (SACClankGadgets.JETBOOTS,),
    SACCases.HIGH_ROLLERS_CASINO:   (SACClankGadgets.HOLOMONOCLE,),
    SACCases.VENANTONIO_LABS:       (),
    SACCases.GALACTIC_BOLT_RESERVE: (SACClankWeapons.THROWTIE, SACClankWeapons.CUFFLINK),
    SACCases.SPACESHIP_GRAVEYARD:   (),
    SACCases.UNDERWATER_BUNKER:     (),
}


def _has_unlock(world: "SecretAgentClankWorld", name: str) -> Has:
    if world.options.progressive_weapons and name in UNLOCK_TO_PROGRESSIVE:
        return Has(UNLOCK_TO_PROGRESSIVE[name])
    return Has(name)


def HasEnemyAccess(world: "SecretAgentClankWorld") -> Rule:
    """Clank can reach enemies in at least one case (see CLANK_ENEMY_CASES)."""
    existing = region_names(world)
    rule = False_()
    for case, items in CLANK_ENEMY_CASES.items():
        if case not in existing:
            continue
        case_rule = CanReachRegion(case)
        for item in items:
            case_rule = case_rule & _has_unlock(world, item)
        rule = rule | case_rule
    return rule


def HasProjectileWeapon() -> Has:
    return Has(SACClankWeapons.THROWTIE) | Has(SACClankWeapons.LIGHTNINGUMBRELLA) | Has(SACClankWeapons.CUFFLINK)


def HasCharacter(world: "SecretAgentClankWorld", character: str) -> Has | True_:
    if world.options.infobots != Infobots.option_character_unlocks:
        return True_()
    if character in CHARACTER_ITEM_NAME:
        return Has(CHARACTER_ITEM_NAME[character])
    return Has(PROGRESSIVE_CHARACTER_ITEM_NAME[character])


def disabled_operatives(world: "SecretAgentClankWorld") -> set[str]:
    """Operatives turned off in the Operatives option; their cases get no regions."""
    return {
        operative for operative in ALL_OPERATIVES
        if operative not in world.options.operatives.value
    }


def case_access_rule(world: "SecretAgentClankWorld", case: "Case") -> Has | True_:
    rule = HasPlanet(world, case.planet) & HasCase(world, case.name)
    if case.operative != SACOperatives.SPECIAL_MISSIONS:
        if (world.options.infobots == Infobots.option_character_unlocks
                and case.operative in PROGRESSIVE_CHARACTER_ITEM_NAME):
            count = list(CASES_BY_OPERATIVE[case.operative]).index(case)
            rule = rule & (Has(PROGRESSIVE_CHARACTER_ITEM_NAME[case.operative], count) if count else True_())
        else:
            rule = rule & HasCharacter(world, case.operative)
    item = CASE_NAME_TO_INFOBOT.get(case.name)
    return rule | Has(item) if item else rule

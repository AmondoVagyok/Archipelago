"""Rule builders, matching worlds/rac_size_matters/rules/_helpers.py's
HasWeapon/HasGadget/HasInfobot pattern (rule_builder.rules objects applied
via world.set_rule(), not plain lambdas). Lives inside rules/ (user:
"rule helpers should live within rules") -- world.py's regions.py imports
case_access_rule()/disabled_operatives() from here via
".rules.rule_helpers", which eagerly loads the whole rules/ package (running
rules/__init__.py, every rules/<case>.py, and entrances.py) before regions.py
finishes its own import. That's NOT a cycle, just wider eager loading: nothing
under rules/ imports regions.py (verified), so nothing here ever waits on
regions.py to finish first.

Gating tiers (see options.py):
  - HasPlanet: planet-level access. Progressive Planet on (regardless of
    Infobots) -> Has(PROGRESSIVE_PLANET_ITEM_NAME, index-in-PLANET_NAMES).
    Otherwise, Infobots=planets -> flat per-planet Access item;
    Infobots=cases -> always True (planet tier skipped, case tier below
    handles it instead). These two tiers are mutually exclusive by design,
    to keep the interaction simple -- not confirmed against user intent
    beyond what was asked, flag if a different interaction was wanted.
  - HasCase: case-level access. Only meaningful under Infobots=cases (and
    Progressive Planet off, see above) -- otherwise always True.
  - HasCharacter: Character Items on -> the character's unlock item
    (flat for Ratchet/Clank, progressive first-copy for Qwark/Gadgetbots).
    Off -> always True. Operatives entirely disabled via the Operatives
    option are NOT handled here -- disabled_operatives()/create_regions()
    exclude their locations from generation outright rather than leaving
    them permanently unreachable (see regions.py's docstring).

case_access_rule() combines HasPlanet + HasCase (+ HasCharacter, with the
same starting-case/Special-Missions exemption) into the one rule that
gates a case's "To <Case>" entrance (see entrances.py) and, for Defeat
Klunk / Qwark Opera, a Victory event's own rule (see regions.py's
_create_victory()) -- both need the exact same "can this case actually be
reached" check, just applied to different things."""
from typing import TYPE_CHECKING

from rule_builder.rules import Has, True_

from ..constants import (
    CASE_NAME_TO_INFOBOT,
    CHARACTER_ITEM_NAME,
    PLANET_ACCESS_ITEM_NAME,
    PLANET_NAMES,
    PROGRESSIVE_CHARACTER_ITEM_NAME,
)
from ..constants.operatives import ALL_OPERATIVES, SACOperatives
from ..items import PROGRESSIVE_PLANET_ITEM_NAME
from ..options import Infobots

if TYPE_CHECKING:
    from ..constants.planets import Case
    from ..world import SecretAgentClankWorld


def HasPlanet(world: "SecretAgentClankWorld", planet: str) -> Has | True_:
    if (world.options.infobots == Infobots.option_progressive_planet):
        index = PLANET_NAMES.index(planet)
        return Has(PROGRESSIVE_PLANET_ITEM_NAME, index) if index else True_()
    if world.options.infobots in (Infobots.option_cases, Infobots.option_character_unlocks):
        return True_()
    item = PLANET_ACCESS_ITEM_NAME.get(planet)
    return Has(item) if item else True_()


def HasCase(world: "SecretAgentClankWorld", case_name: str) -> Has | True_:
    if (world.options.infobots == Infobots.option_progressive_planet) or world.options.infobots != Infobots.option_cases:
        return True_()
    item = CASE_NAME_TO_INFOBOT.get(case_name)
    return Has(item) if item else True_()


def HasWeapon(weapon: str) -> Has:
    from ..constants.weapon_progression import UNLOCK_TO_PROGRESSIVE
    progressive = UNLOCK_TO_PROGRESSIVE.get(weapon)
    return Has(weapon) | Has(progressive) if progressive else Has(weapon)


def HasGadget(gadget: str) -> Has:
    from ..constants.weapon_progression import UNLOCK_TO_PROGRESSIVE
    progressive = UNLOCK_TO_PROGRESSIVE.get(gadget)
    return Has(gadget) | Has(progressive) if progressive else Has(gadget)


def HasCharacter(world: "SecretAgentClankWorld", character: str) -> Has | True_:
    if not (world.options.infobots == Infobots.option_character_unlocks):
        return True_()
    if character in CHARACTER_ITEM_NAME:
        return Has(CHARACTER_ITEM_NAME[character])
    return Has(PROGRESSIVE_CHARACTER_ITEM_NAME[character])


def disabled_operatives(world: "SecretAgentClankWorld") -> set[str]:
    """Operatives removed entirely via options.py's Operatives option --
    shared by regions.py's create_regions() (to skip their cases'
    regions/locations outright) and entrances.py's set_entrance_rules()
    (to skip setting a rule on an entrance that was never created).
    ItemDict (Operatives) culls 0-valued entries in its own __init__, so
    "set to 0" and "removed from the list" both collapse to "key absent
    from .value" -- there's no way to see an explicit 0 here. Covers all
    5 operatives, Special Missions included (user: "lets change characters
    to Operatives. we will have special missions here aswel as an
    operative") -- see constants/operatives.py's module docstring for why
    that's a separate concern from HasCharacter's per-case unlock-item
    gate below, which still exempts Special Missions."""
    return {
        operative for operative in ALL_OPERATIVES
        if operative not in world.options.operatives.value
    }


def case_access_rule(world: "SecretAgentClankWorld", case: "Case") -> Has | True_:
    rule = HasPlanet(world, case.planet) & HasCase(world, case.name)
    if case.operative != SACOperatives.SPECIAL_MISSIONS:
        if (world.options.infobots == Infobots.option_character_unlocks
                and case.operative in PROGRESSIVE_CHARACTER_ITEM_NAME):
            from ..constants.planets import CASES_BY_OPERATIVE
            # 0-based index into that operative's own case list -- the Nth
            # case needs N PRIOR copies already owned, same convention as
            # HasPlanet's Progressive Planet count above. count = index + 1
            # was self-referential: the last case's own Progressive copy is
            # itself one of the exact number of copies that formula demanded
            # to reach it, an unreachable location no fill could ever place
            # that copy into (confirmed live via
            # test_qwark_only_fills_with_an_accessible_native_start's
            # Fill.FillError).
            count = list(CASES_BY_OPERATIVE[case.operative]).index(case)
            rule = rule & (Has(PROGRESSIVE_CHARACTER_ITEM_NAME[case.operative], count) if count else True_())
        else:
            rule = rule & HasCharacter(world, case.operative)
    # The seed precollects its starting case file in every access mode.
    # Explicit case files agree with resolve_owned_cases client-side.
    item = CASE_NAME_TO_INFOBOT.get(case.name)
    return rule | Has(item) if item else rule

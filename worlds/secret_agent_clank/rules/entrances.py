"""Case access -- mirrors worlds/rac_size_matters/rules/entrances.py's
per-planet pattern, at SAC's per-case granularity: one "To <Case>"
entrance per case (created in regions.py, empty of a rule until now),
gated here by that case's real access requirement.

case_access_rule() (see rule_helpers.py) combines the two independent
option tiers (see options.py's Infobots): Infobots=planets means owning a
planet's Access item grants every one of its cases at once (HasPlanet
real, HasCase a no-op True_()); Infobots=cases means each case needs its
own Case File item individually (HasPlanet a no-op True_(), HasCase
real) -- ANDing both together, unconditionally, gets whichever behavior
is actually active without this module needing to know which tier is
selected itself."""
from typing import TYPE_CHECKING

from ..constants.planets import ALL_CASES
from .rule_helpers import case_access_rule, disabled_operatives

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld


def set_entrance_rules(world: "SecretAgentClankWorld") -> None:
    player = world.player
    mw = world.multiworld
    disabled = disabled_operatives(world)

    for case in ALL_CASES:
        if case.operative in disabled:
            continue
        world.set_rule(mw.get_entrance(f"To {case.name}", player), case_access_rule(world, case))

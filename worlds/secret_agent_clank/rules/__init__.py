"""Location rules live on each SACLocation record in its case file (locations/<case>.py); this package keeps the
shared rule builders (rule_helpers.py), case access (entrances.py) and the vendor routes (vendor_access.py) --
mirrors worlds/rac_size_matters/rules' layout."""
from typing import TYPE_CHECKING

from rule_builder.rules import Has

from .entrances import set_entrance_rules
from .rule_helpers import HasCase, HasCharacter, HasPlanet
from .vendor_access import set_vendor_rules

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld

__all__ = ["HasCase", "HasCharacter", "HasPlanet", "set_rules"]


def set_rules(world: "SecretAgentClankWorld") -> None:
    from ..locations import CASE_LOCATIONS

    world.set_completion_rule(Has("Victory"))

    set_entrance_rules(world)

    locations = {location.name: location for location in world.multiworld.get_locations(world.player)}
    for definition in CASE_LOCATIONS:
        location = locations.get(definition.name)
        if location is not None and definition.rule is not None:
            world.set_rule(location, definition.rule(world))
    set_vendor_rules(world)

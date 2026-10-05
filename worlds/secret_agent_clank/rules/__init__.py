"""Applies access rules. Per-location rules live on the records in locations/<case>.py."""
from typing import TYPE_CHECKING

from rule_builder.rules import Has

from .entrances import set_entrance_rules
from .rule_helpers import HasCase, HasCharacter, HasPlanet
from .vendor_access import set_vendor_rules

if TYPE_CHECKING:
    from ..world import SecretAgentClankWorld

__all__ = ["HasCase", "HasCharacter", "HasPlanet", "set_rules"]


def set_rules(world: "SecretAgentClankWorld") -> None:
    # Imported here: the per-case location files import this package for their rules.
    from ..locations import CASE_LOCATIONS

    world.set_completion_rule(Has("Victory"))

    set_entrance_rules(world)

    locations = {location.name: location for location in world.multiworld.get_locations(world.player)}
    for definition in CASE_LOCATIONS:
        location = locations.get(definition.name)
        rule = definition.resolve_rule(world) if location is not None else None
        if rule is not None:
            world.set_rule(location, rule)
    set_vendor_rules(world)

"""Item and location classes, kept out of world.py so regions.py can import them without a cycle."""
from BaseClasses import Item, Location


class SACItem(Item):
    game: str = "Secret Agent Clank"


class SACLocation(Location):
    game: str = "Secret Agent Clank"

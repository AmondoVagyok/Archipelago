"""Weapon quick-select wheel tracking. Read-only for now -- this doesn't
drive any AP location yet, since RATCHET_WEAPONS' real weapon id/name
mapping isn't known (see constants/weapons.py). Its purpose right now is
reverse-engineering that mapping: /states (see
client/command_processor.py) prints the current slot ids, so cycling
weapons in-game and watching which id shows up in which slot is how the
real names get matched to ids."""
from typing import TYPE_CHECKING

from .address_maps import QUICK_SELECT_ADDRESS, QUICK_SELECT_SLOT_COUNT

if TYPE_CHECKING:
    from ..pypine import Pine


class QuickSelectState:

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine

    @property
    def slots(self) -> list[int]:
        """The weapon id currently bound to each of the 8 wheel slots, in
        slot order."""
        return [
            self.pine.read_int32(QUICK_SELECT_ADDRESS + slot * 4)
            for slot in range(QUICK_SELECT_SLOT_COUNT)
        ]

    def __repr__(self) -> str:
        return f"QuickSelectState(slots={self.slots!r})"

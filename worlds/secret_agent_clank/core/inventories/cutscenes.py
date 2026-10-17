from typing import TYPE_CHECKING

from ...constants import CUTSCENE_FLAGS
from .case_events import EventFlagInventory

if TYPE_CHECKING:
    from ...pypine import Pine


class CutsceneInventory(EventFlagInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, CUTSCENE_FLAGS)

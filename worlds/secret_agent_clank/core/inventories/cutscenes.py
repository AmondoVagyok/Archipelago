"""Cutscene location tracking; flags are in constants/cutscenes.py."""
from typing import TYPE_CHECKING

from ...constants.cutscenes import CUTSCENES
from .case_events import CaseEventInventory

if TYPE_CHECKING:
    from ...pypine import Pine


class CutsceneInventory(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, CUTSCENES)

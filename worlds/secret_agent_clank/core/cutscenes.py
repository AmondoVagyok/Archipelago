"""Cutscene-trigger tracking -- see constants/cutscenes.py's CUTSCENES for
the per-cutscene case/address/flag data (CONFIRMED live for every entry).
Baselines only once, from CaseEventInventory's initial dict.fromkeys(...,
False) state -- core/core.py deliberately never calls sync() for this one,
unlike the challenge Inventories: an entry cutscene (e.g. Boltaire
Museum's) can trigger the instant its case becomes ready, so baselining on
every transition would eat that exact 0->1 transition before check() ever
saw it as new. TODO: means a reconnect after already seeing a cutscene
this session re-reports it as new; not handled yet."""
from typing import TYPE_CHECKING

from ..constants.cutscenes import CUTSCENES
from .case_events import CaseEventInventory

if TYPE_CHECKING:
    from ..pypine import Pine


class CutsceneInventory(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, CUTSCENES)

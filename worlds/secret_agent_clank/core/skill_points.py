"""Skill point tracking -- see constants/skillpoints.py's SKILL_POINTS for
the per-skill-point case/address/flag data (CONFIRMED live for all 65).
Upgraded from a running-total counter (the old SKILL_POINTS_ADDRESS-based
approach, which could only report "the total went up") now that individual
address/flag data is confirmed for every skill point."""
from typing import TYPE_CHECKING

from ..constants.skillpoints import SKILL_POINTS
from .inventories.case_events import CaseEventInventory

if TYPE_CHECKING:
    from ..pypine import Pine


class SkillPointState(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, SKILL_POINTS)

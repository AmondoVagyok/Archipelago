"""Special Challenge tracking; addresses are in constants/special_challenges.py."""
from typing import TYPE_CHECKING

from ...constants.special_challenges import SPECIAL_CHALLENGES
from .case_events import CaseEventInventory

if TYPE_CHECKING:
    from ...pypine import Pine


class SpecialChallengeInventory(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, SPECIAL_CHALLENGES)

    def sync(self) -> None:
        """Saved completions remain pending until AP accepts their checks."""
        pass

    def check(self) -> list[str]:
        return [str(entry) for entry in self.entries
                if not self.completed[str(entry)] and self.get(entry)]

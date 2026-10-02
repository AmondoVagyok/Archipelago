"""Gadgetbot Challenge tracking; addresses are in constants/gadgetbot_challenges.py."""
from typing import TYPE_CHECKING

from ...constants.gadgetbot_challenges import GADGETBOT_CHALLENGES
from .case_events import CaseEventInventory

if TYPE_CHECKING:
    from ...pypine import Pine


class GadgetbotChallengeInventory(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, GADGETBOT_CHALLENGES)

"""Gadgetbot Challenge tracking; flags are in constants/gadgetbot_challenges.py."""
from typing import TYPE_CHECKING

from ...constants.gadgetbot_challenges import GADGETBOT_CHALLENGE_FLAGS
from .case_events import EventFlagInventory

if TYPE_CHECKING:
    from ...pypine import Pine


class GadgetbotChallengeInventory(EventFlagInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, GADGETBOT_CHALLENGE_FLAGS)

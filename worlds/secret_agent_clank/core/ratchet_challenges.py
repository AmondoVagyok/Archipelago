"""Ratchet Challenge completion tracking -- the Ratchet-operative
counterpart to core/gadgetbot_challenges.py's GadgetbotChallengeInventory
and core/special_challenges.py's SpecialChallengeInventory -- see
constants/ratchet_challenges.py's RATCHET_CHALLENGES for the per-challenge
case/address data."""
from typing import TYPE_CHECKING

from ..constants.ratchet_challenges import RATCHET_CHALLENGES
from .case_events import CaseEventInventory

if TYPE_CHECKING:
    from ..pypine import Pine


class RatchetChallengeInventory(CaseEventInventory):

    def __init__(self, pine: "Pine") -> None:
        super().__init__(pine, RATCHET_CHALLENGES)

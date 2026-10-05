import unittest

from ..constants.special_challenges import SPECIAL_CHALLENGE_FLAGS
from ..core.inventories.special_challenges import SpecialChallengeInventory
from .test_runtime import Memory


class SpecialChallengeTests(unittest.TestCase):
    def test_saved_canals_completions_survive_sync_and_retry(self):
        memory = Memory()
        tracker = SpecialChallengeInventory(memory)
        canals = list(SPECIAL_CHALLENGE_FLAGS.items())[:3]
        for _, flag in canals:
            memory.data[flag.address] = 1
        expected = [name for name, _ in canals]
        tracker.sync()
        self.assertEqual(tracker.check(), expected)
        tracker.sync()
        self.assertEqual(tracker.check(), expected)
        tracker.confirm(expected[0])
        self.assertEqual(tracker.check(), expected[1:])
        tracker.sync_from_ap(set(expected))
        self.assertEqual(tracker.check(), [])

    def test_confirmed_checks_stay_confirmed_across_save_changes(self):
        memory = Memory()
        tracker = SpecialChallengeInventory(memory)
        name, flag = next(iter(SPECIAL_CHALLENGE_FLAGS.items()))
        tracker.confirm(name)
        tracker.check()
        memory.data[flag.address] = 1
        tracker.sync()
        self.assertEqual(tracker.check(), [])

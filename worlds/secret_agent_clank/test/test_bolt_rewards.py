import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from ..core.bolt_rewards import BoltRewards, reward_balance
from ..core.address_maps import BOLTS_ADDRESS
from ..core.core import Core
from .test_runtime import Memory


class BoltRewardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.temp.cleanup)
        self.p = Memory()
        self.p.write_int32 = lambda a, n: self.p.batch_write_int32([(a, n)])
        self.p.write_int32(BOLTS_ADDRESS, 1000)
        self.r = BoltRewards(self.p, Mock())
        self.r.configure('seed', 0, 1, self.temp.name)

    def test_percentage_rounding_compounding_and_zero(self):
        self.assertEqual(reward_balance(1000, 2), 1440)
        self.assertEqual(reward_balance(491, 1), 589)
        self.assertEqual(reward_balance(0, 3), 0)

    def test_starting_grant_precedes_rewards_and_survives_restart(self):
        self.r.configure('seed', 0, 1, self.temp.name, starting_bolts=5000)
        self.r.received = 1
        self.r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 7200)
        self.p.write_int32(BOLTS_ADDRESS, 200)
        r = BoltRewards(self.p, Mock())
        r.configure('seed', 0, 1, self.temp.name, starting_bolts=5000)
        r.received = 1
        r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 200)

    def test_starting_grant_lost_ack_recovers_after_restart(self):
        self.r.configure('seed', 0, 1, self.temp.name, starting_bolts=5000)
        original = self.p.write_int32
        def lost_ack(a, n):
            original(a, n)
            raise OSError('Lost acknowledgement')
        self.p.write_int32 = lost_ack
        with self.assertRaises(OSError):
            self.r.deliver()
        self.p.write_int32 = original
        r = BoltRewards(self.p, Mock())
        r.configure('seed', 0, 1, self.temp.name, starting_bolts=5000)
        r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 6000)
        self.assertTrue(r.state['starting_delivered'])

    def test_existing_reward_journal_receives_missing_starting_grant(self):
        self.r.state = {'delivered': 2, 'pending': None}
        self.r._save()
        r = BoltRewards(self.p, Mock())
        r.configure('seed', 0, 1, self.temp.name, starting_bolts=5000)
        r.received = 2
        r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 6000)
        self.assertEqual(r.state['delivered'], 2)

    def test_duplicate_packets_and_restart_do_not_reaward(self):
        self.r.received = 2
        self.r.deliver()
        self.r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 1440)
        r = BoltRewards(self.p, Mock())
        r.configure('seed', 0, 1, self.temp.name)
        self.p.write_int32(BOLTS_ADDRESS, 500)  # Purchased something.
        r.received = 2
        r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 500)
        r.received = 3
        r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 600)

    def test_delivery_waits_for_game_readiness(self):
        core = Core(self.p)
        core.bolt_rewards = self.r
        core.native_runtime.service = Mock(return_value=False)
        core.case.check_transition = Mock(return_value=False)
        core.apply_inventory(ratchet={}, clank={}, received_names=['Bolts', 'Bolts'])
        core.tick()
        self.assertEqual(self.r.received, 2)
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 1000)
        self.assertFalse(self.r.path.exists())

    def test_lost_write_ack_recovers_without_duplicate(self):
        original = self.p.write_int32
        def lost_ack(a, n):
            original(a, n)
            raise OSError('Lost acknowledgement')
        self.p.write_int32 = lost_ack
        self.r.received = 1
        with self.assertRaises(OSError):
            self.r.deliver()
        self.p.write_int32 = original
        self.r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 1200)
        self.assertEqual(self.r.state['delivered'], 1)

    def test_separate_slot_has_separate_journal(self):
        self.r.received = 1
        self.r.deliver()
        self.r.configure('seed', 0, 2, self.temp.name)
        self.r.received = 1
        self.r.deliver()
        self.assertEqual(self.p.read_int32(BOLTS_ADDRESS), 1440)

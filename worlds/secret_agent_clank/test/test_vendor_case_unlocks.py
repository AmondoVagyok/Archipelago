from ..constants.vendor import vendor_location_name
"""Vendor checks are independent of case unlocks and gameplay ownership."""
import unittest
from unittest.mock import patch

from ..constants.clank_gadgets import SACClankWeapons
from ..core.patches import MARKER, LocationHooks
from ..core.patches.plan import PatchPlan
from .test_runtime import Memory


class VendorPurchaseStateTests(unittest.TestCase):
    def test_native_names_are_normalized_before_plan_creation(self):
        hooks = LocationHooks(Memory())
        plan = PatchPlan([], {}, {})
        with patch("worlds.secret_agent_clank.core.patches.hooks.VendorOnly.prepare", return_value=plan) as prepare:
            hooks.prepare({}, pickup_locations={}, vendor_locations={14: "HoloKnuckles"},
                          checked={vendor_location_name(SACClankWeapons.HOLOKNUCKLES)})
        self.assertEqual(prepare.call_args.args[1], {14: vendor_location_name(SACClankWeapons.HOLOKNUCKLES)})
        self.assertEqual(prepare.call_args.args[2], {vendor_location_name(SACClankWeapons.HOLOKNUCKLES)})

    def test_server_acknowledgement_suppresses_the_native_offer(self):
        p = Memory()
        hooks = LocationHooks(p)
        hooks.installed, hooks.module, hooks.marker_address = True, 1, 0x120000
        p.data[0x120000:0x120000 + len(MARKER)] = MARKER
        p.batch_write_int32([(0x206328, 1)])
        hooks.tables = {"vendor": 0x130000}
        hooks.locations = {"vendor": {14: vendor_location_name(SACClankWeapons.HOLOKNUCKLES)}}
        p.batch_write_int8([(0x13000E, 1)])
        hooks.sync_checked({vendor_location_name(SACClankWeapons.HOLOKNUCKLES)})
        self.assertEqual(p.read_int8(0x13000E), 2)
        self.assertEqual(hooks.poll(), [])
        p.batch_write_int32([(0x206328, 2)])
        p.writes.clear()
        hooks.sync_checked({vendor_location_name(SACClankWeapons.HOLOKNUCKLES)})
        self.assertEqual(p.writes, [])

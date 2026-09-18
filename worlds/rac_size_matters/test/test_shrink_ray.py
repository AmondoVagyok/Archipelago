import json
import struct
import unittest
from pathlib import Path

from .test_native_patches import Memory
from ..constants.shrink_ray import SHRINK_RAY_PUZZLE_BITS, SHRINK_RAY_LOCATION_PLANETS
from ..core.shrink_ray import ShrinkRaySkipInventory
from ..core.address_maps import SHRINK_RAY_GATE_ADDRESS
from ..core.patches import shrink_ray


class ShrinkMemory(Memory):
    def read_int16(self, address):
        return struct.unpack_from('<H', self.data, address)[0]

    def write_int16(self, address, value):
        self.write_bytes(address, struct.pack('<H', value))


class TestShrinkRay(unittest.TestCase):
    def test_native_bits_and_planet_scope(self):
        names = list(SHRINK_RAY_PUZZLE_BITS)
        for name, puzzle_id in zip(names, (0, 1, 4, 6, 7, 9, 10)):
            with self.subTest(name=name):
                memory = ShrinkMemory()
                inventory = ShrinkRaySkipInventory(memory)
                memory.write_int16(SHRINK_RAY_GATE_ADDRESS, 1 << puzzle_id)
                memory.writes.clear()
                self.assertEqual(inventory.check(1), [])
                self.assertEqual(inventory.check(SHRINK_RAY_LOCATION_PLANETS[name]), [name])
                self.assertEqual(inventory.check(SHRINK_RAY_LOCATION_PLANETS[name]), [])
                self.assertEqual(memory.writes, [])

    def test_unrelated_challenge_is_not_completion(self):
        memory = ShrinkMemory()
        memory.write_int8(0x1F4B3EF, 1)
        inventory = ShrinkRaySkipInventory(memory)
        self.assertEqual(inventory.check(3), [])
        memory.write_int16(SHRINK_RAY_GATE_ADDRESS, 0x200)
        inventory.force_outpost_omega_open()
        self.assertEqual(memory.read_int16(SHRINK_RAY_GATE_ADDRESS), 0x204)

    def test_ap_sync(self):
        memory = ShrinkMemory()
        inventory = ShrinkRaySkipInventory(memory)
        name = next(iter(SHRINK_RAY_PUZZLE_BITS))
        inventory.sync_from_ap({name, 'unrelated'})
        memory.write_int16(SHRINK_RAY_GATE_ADDRESS, 1)
        self.assertEqual(inventory.check(3), [])
        self.assertEqual(inventory.completed, {name})

    def test_retail_door_bypass_without_save_or_code_writes(self):
        fixtures = json.loads((Path(__file__).parent / 'fixtures/shrink_ray_us.json').read_text())
        for name, row in fixtures.items():
            with self.subTest(planet=name):
                memory = ShrinkMemory()
                for address, data in row['segments']:
                    memory.write_bytes(address, bytes.fromhex(data))
                for moby, rt, puzzle in row['locks']:
                    memory.write_int32(rt + 0x4C, 0)
                    memory.write_int8(rt + 0x50, 1)
                inventory = ShrinkRaySkipInventory(memory)
                base = row['base']
                inventory.bind(3, base, memory.read_bytes(base, 0x240000))
                memory.writes.clear()
                inventory.set_skip(3, False)
                inventory.set_skip(7, True)
                self.assertEqual(memory.writes, [])
                inventory.set_skip(3, True)
                self.assertEqual(len(inventory.plan.locks), len(row['locks']))
                for moby, rt, puzzle in row['locks']:
                    self.assertEqual(memory.read_int8(rt + 0x50), 0)
                count = len(memory.writes)
                inventory.set_skip(3, True)
                self.assertEqual(len(memory.writes), count)
                inventory.set_skip(3, False)
                self.assertTrue(all(address in {rt + 0x50 for _, rt, _ in row['locks']}
                                    for address, _ in memory.writes))
                for moby, rt, puzzle in row['locks']:
                    self.assertEqual(memory.read_int8(rt + 0x50), 1)
                self.assertEqual(inventory.check(3), [])
                rt = row['locks'][0][1]
                memory.write_int32(rt + 0x4C, 1)
                inventory.set_skip(3, True)
                self.assertEqual(memory.read_int8(rt + 0x50), 1)
                memory.write_int32(rt + 0x4C, 0)
                inventory.set_skip(3, True)
                self.assertEqual(memory.read_int8(rt + 0x50), 0)
                memory.write_int32(rt + 4, 0)
                memory.writes.clear()
                with self.assertRaises(RuntimeError):
                    inventory.set_skip(3, True)
                self.assertEqual(memory.writes, [])

    def test_no_lock(self):
        self.assertIsNone(shrink_ray.prepare(ShrinkMemory(), code_start=0xD00000, code=bytes(256)))

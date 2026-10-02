import unittest
from types import SimpleNamespace
from unittest.mock import patch

from ..constants.native_functions import NativeFunctions
from ..core.patches.asm import Patch, jump
from ..core.patches.progression import Progression
from ..core.patches.storage import free_blocks, plan_storage, storage_address
from ..core.patches.vendor_catalog import VendorCatalog
from .mips_cpu import CPU
from .test_native_capture_plans import CaptureMemory
from .test_runtime import Memory


class HookStorageTests(unittest.TestCase):
    def test_plan_reserves_large_blocks_before_small_counter(self):
        ranges = [(0x1000, 0x1020), (0x2000, 0x2008)]
        self.assertEqual(plan_storage(ranges, [], [4, 32]), [0x2000, 0x1000])

    def test_plan_backtracks_instead_of_stranding_final_hook(self):
        # Greedy best fit puts 24 in 28 and 20 in 32, stranding the last 8.
        # A complete plan puts 24+8 in 32 and 20+8 in 28.
        ranges = [(0x1000, 0x101C), (0x2000, 0x2020)]
        sizes = [24, 20, 8, 8]
        addresses = plan_storage(ranges, [], sizes)
        self.assertIsNotNone(addresses)
        spans = sorted((address, address + size) for address, size in zip(addresses, sizes))
        self.assertTrue(all(b <= c for (_, b), (c, _) in zip(spans, spans[1:])))
        self.assertTrue(all(any(start <= a < b <= end for start, end in ranges) for a, b in spans))

    def test_impossible_plan_returns_no_partial_allocation(self):
        self.assertIsNone(plan_storage([(0x1000, 0x1020)], [], [20, 16]))

    def test_split_manual_guard_rejects_invalid_slots_without_touching_stack(self):
        p = CaptureMemory()
        def allocate(code):
            p.write_bytes(0x160000, code)
            return 0x160000
        code = Progression.manual_xp_guard(0x100000, 0x120000, 0x150000, allocate)
        p.write_bytes(0x140000, code)
        for slot in (40, 255, 0xFFFFFFFF):
            cpu = CPU(p)
            cpu.r[4:7] = [slot, 50, 1]
            stack = cpu.r[29]
            cpu.run(0x140000)
            self.assertEqual(cpu.r[4:7], [slot, 50, 1])
            self.assertEqual(cpu.r[29], stack)
            self.assertEqual(cpu.r[2], 0)

    def test_small_hooks_preserve_room_for_cap_table(self):
        ranges = [(0x1000, 0x102C), (0x2000, 0x2024)]
        address = storage_address(ranges, [], 28)
        self.assertEqual(address, 0x2000)
        patches = [Patch(address, bytes(28), bytes(28))]
        self.assertEqual(storage_address(ranges, patches, 40), 0x1000)

    def test_alignment_and_overlapping_occupied_spans(self):
        patches = [Patch(0x1008, bytes(12), bytes(12)),
                   Patch(0x1010, bytes(12), bytes(12))]
        self.assertEqual(free_blocks([(0x1001, 0x1028)], patches),
                         [(0x1004, 0x1008), (0x101C, 0x1028)])
        self.assertEqual(storage_address([(0x1001, 0x1028)], patches, 12), 0x101C)
        self.assertIsNone(storage_address([(0x1001, 0x1028)], patches, 16))

    def test_catalog_shares_only_tail_after_full_row_buffer(self):
        p = Memory()
        buy, builder, begin, add, end = 0x100000, 0x110000, 0x120000, 0x130000, 0x140000
        symbols = {NativeFunctions.SCRNVENDOR_PROCESS_PURCHASE: buy,
                   "ICONMENU_BeginAddingMenuItems__FP9tICONMENUPvUi": begin,
                   "ICONMENU_AddItem__FP9tICONMENUUiUiUiUiUiUi": add,
                   "ICONMENU_EndAddingMenuItems__FP9tICONMENU": end}
        guards = {0: 0x27BDFF70, 0x4C: jump(begin, True), 0x54: 0x27A20010,
                  0x70: 0x24020011, 0x300: jump(add, True), 0x43C: jump(add, True),
                  0x4DC: jump(add, True), 0x660: jump(add, True), 0x6FC: jump(add, True),
                  0x24: 0x24840000, 0x58: 0x3C030000, 0x60: 0x3C020000,
                  0x64: 0xA0600000, 0x68: 0xA0400000, 0x740: jump(end, True)}
        p.batch_write_int32([(builder + offset, word) for offset, word in guards.items()])
        p.write_int32(buy + 0x338, jump(builder, True))
        hooks = SimpleNamespace(patches=[], locations={}, tables={}, extra_ranges=[])
        p.writes.clear()
        catalog = VendorCatalog(p)
        # This fixture models only the catalog. Native tab code and storage
        # signatures are exercised against real captures in test_vendor_tabs.
        with patch('worlds.secret_agent_clank.core.patches.vendor_catalog.VendorTabs.prepare',
                   return_value=([], bytes(8))):
            hooks.patches.extend(catalog.prepare(symbols, hooks))
        payload = catalog.patches[0]
        self.assertEqual(hooks.extra_ranges,
                         [(builder + len(payload.replacement), builder + catalog.END)])
        self.assertEqual(payload.replacement[-41 * catalog.ROW_SIZE:], bytes(41 * catalog.ROW_SIZE))
        # Manual XP wrappers need a contiguous block larger than a debug stub.
        address = storage_address(hooks.extra_ranges, hooks.patches, 120)
        self.assertEqual(address, builder + len(payload.replacement))
        self.assertLessEqual(address + 120, builder + catalog.END)
        self.assertEqual(p.writes, [])

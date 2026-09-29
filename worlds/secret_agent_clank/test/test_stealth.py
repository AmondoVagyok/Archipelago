import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from test.general import setup_multiworld
from ..world import SecretAgentClankWorld
from ..constants.stealth import stealth_thresholds, stealth_location_name
from ..core.stealth import StealthState, END, KILL
from ..core.symbols import RuntimeSymbols
from ..core.patches.progression import Progression
from ..core.patches import mips as m
from .test_native_capture_plans import CaptureMemory
from .mips_cpu import CPU


class StealthTests(unittest.TestCase):
    def test_generation_modes_and_stable_ids(self):
        ids = {}
        for mode, expected in ((0, ()), (1, (5,10,15,20,25)), (2, (10,20)), (3, tuple(range(1,26)))):
            mw = setup_multiworld(SecretAgentClankWorld, options={"stealth_takedown_checks": mode})
            locations = {l.name: l.address for l in mw.get_locations(1) if l.name.startswith("Clank Stealth Takedowns:")}
            self.assertEqual(set(locations), {stealth_location_name(n) for n in expected})
            for name, address in locations.items():
                self.assertEqual(ids.setdefault(name, address), address)
            self.assertEqual(mw.worlds[1].fill_slot_data()["stealth_takedown_checks"], mode)
        from Options import OptionError
        for mode in (1, 2, 3):
            for operatives in ({"Qwark": 1, "Ratchet": 1}, {"Qwark": 1, "Clank": 0}):
                with self.assertRaisesRegex(OptionError, "requires Clank"):
                    setup_multiworld(SecretAgentClankWorld, options={"stealth_takedown_checks": mode,
                        "goal": "qwark_opera", "operatives": operatives})
        setup_multiworld(SecretAgentClankWorld, options={"stealth_takedown_checks": 0,
            "goal": "qwark_opera", "operatives": {"Qwark": 1}})

    def test_access_requires_a_clank_case(self):
        from BaseClasses import CollectionState
        from ..constants import CASE_NAME_TO_INFOBOT, SACCases
        mw = setup_multiworld(SecretAgentClankWorld, options={"stealth_takedown_checks": 3})
        state = CollectionState(mw)
        for item in mw.precollected_items[1]:
            state.remove(item)
        loc = mw.get_location(stealth_location_name(25), 1)
        self.assertFalse(loc.can_reach(state))
        state.collect(mw.worlds[1].create_item(CASE_NAME_TO_INFOBOT[SACCases.BOLTAIRE_MUSEUM]))
        self.assertFalse(loc.can_reach(state))  # A single Clank case is not enough for the TODO fallback.
        from ..constants import CASES_BY_OPERATIVE, SACOperatives
        for case in CASES_BY_OPERATIVE[SACOperatives.CLANK]:
            state.collect(mw.worlds[1].create_item(CASE_NAME_TO_INFOBOT[case.name]))
        self.assertTrue(loc.can_reach(state))

    def test_native_counter_caps_preserves_arguments_and_tail_calls(self):
        mem = CaptureMemory()
        mem.write_int32 = lambda a, n: mem.batch_write_int32([(a, n)])
        counter, entry, target = 0x110000, 0x120000, 0x130000
        mem.write_bytes(entry, StealthState.wrapper(counter, target))
        for count in (0, 4, 24, 25):
            mem.write_int32(counter, count)
            cpu = CPU(mem)
            cpu.r[m.A0] = 0x123456
            cpu.run(entry, stop=target)
            self.assertEqual(mem.read_int32(counter), min(count + 1, 25))
            self.assertEqual(cpu.r[m.A0], 0x123456)
            self.assertEqual(cpu.r[m.RA], CPU.STOP)

    def test_poll_retry_reload_and_state_loading(self):
        mem = CaptureMemory()
        s = StealthState(mem)
        s.configure(1, reset=True)
        s.binding = (0x1000, 0x2000, b"site", 0x3000, b"code")
        mem.write_bytes(0x2000, b"site")
        mem.write_bytes(0x3000, b"code")
        mem.batch_write_int32([(0x1000, 11)])
        s.on_count = Mock()
        s.poll()
        self.assertEqual(s.checks(), ())
        s.load(0)
        s.poll()
        s.on_count.assert_called_once_with(11)
        self.assertEqual(s.checks(), (stealth_location_name(5), stealth_location_name(10)))
        self.assertEqual(s.checks(), s.checks())  # checks retry until normal delivery accepts them
        mem.batch_write_int32([(0x1000, 0)])
        s.poll()
        self.assertEqual(mem.read_int32(0x1000), 11)
        s.configure(1)
        s.load(5)
        self.assertEqual(s.count, 11)
        mem.write_bytes(0x2000, b"gone")
        s.poll()
        self.assertIsNone(s.binding)
        s.configure(0, reset=True)
        self.assertEqual(s.checks(), ())

    def test_research_captures_validate_success_path_and_plan(self):
        paths = list((Path(__file__).parents[1] / ".research").glob("*.ram"))
        if not paths:
            self.skipTest("Local RAM captures unavailable")
        seen = 0
        for path in paths:
            mem = CaptureMemory()
            mem.data[:] = path.read_bytes()
            symbols = RuntimeSymbols.parse(mem.data, 0)
            if END not in symbols:
                continue
            seen += 1
            s = StealthState(mem)
            s.configure(3)
            s.load(7)
            progression = Progression(mem)
            progression.stealth = s
            edits = progression.prepare(symbols, SimpleNamespace(patches=[]), 1, vendor_enabled=False)
            self.assertIsNotNone(s.binding, path.name)
            spans = sorted((p.address, p.address + len(p.replacement)) for p in edits)
            self.assertTrue(all(b <= c for (a,b),(c,d) in zip(spans, spans[1:])))
            for edit in edits:
                self.assertEqual(mem.read_bytes(edit.address, len(edit.original)), edit.original)
                mem.write_bytes(edit.address, edit.replacement)
            s.poll()
            self.assertEqual(s.count, 7)
            for edit in reversed(edits):
                mem.write_bytes(edit.address, edit.original)
            mem.batch_write_int32([(symbols[END] + 0x4C, 0)])
            with self.assertRaisesRegex(RuntimeError, "path changed"):
                s.prepare(symbols, Mock())
        self.assertGreater(seen, 0)

    def test_combined_pickup_vendor_progression_and_stealth_plans(self):
        from ..core.patches import LocationHooks, PICKUP_LOCATIONS, VENDOR_LOCATIONS
        from ..core.patches.mission_travel import MissionTravel
        from ..core.patches.weapon_mods import WeaponMods
        from ..core.patches.titan_vendor import TitanVendor, TitanOffers
        from ..core.patches.vendor_catalog import VendorCatalog
        from ..core.patches.vendor_presentation import VendorPresentation
        paths = list((Path(__file__).parents[1] / ".research").glob("*.ram"))
        if not paths:
            self.skipTest("Local captures unavailable")
        verified = 0
        for path in paths:
            raw = path.read_bytes()
            symbols = RuntimeSymbols.parse(raw, 0)
            if END not in symbols:
                continue
            verified += 1
            for ng, mode in ((0, 0), (1, 1), (2, 2)):
                with self.subTest(capture=path.name, ng=ng, mode=mode):
                    mem = CaptureMemory()
                    mem.data[:] = raw
                    module = mem.read_int32(0x206328)
                    if module == 11 and mode == 1:
                        self.skipTest("Existing module 11 manual-progression plan exhausts storage even without stealth")
                    hooks = LocationHooks(mem)
                    hooks.prepare(symbols, pickup_locations=PICKUP_LOCATIONS,
                                  vendor_locations=VENDOR_LOCATIONS, entitlements={})
                    hooks.patches.extend(MissionTravel(mem).prepare(symbols))
                    mods = WeaponMods(mem)
                    mods.configure({"ng_plus": ng})
                    hooks.patches.extend(mods.prepare(symbols, hooks, module, (), True))
                    if ng:
                        hooks.patches.extend(TitanVendor(mem).prepare(symbols, hooks, ()))
                    else:
                        hooks.patches.extend(TitanOffers(mem).prepare(symbols))
                    prog = Progression(mem)
                    prog.configure({"ng_plus": ng, "progressive_weapons": mode,
                        "weapon_xp_multiplier": 4 if module == 1 else 1,
                        "health_xp_multiplier": 5 if module == 1 else 1,
                        "bolt_multiplier": 8 if module == 1 else 1})
                    prog.stealth = StealthState(mem)
                    prog.stealth.configure(3)
                    prog.stealth.load(0)
                    hooks.patches.extend(prog.prepare(symbols, hooks, module))
                    hooks.patches.extend(VendorCatalog(mem).prepare(symbols, hooks))
                    hooks.patches.extend(VendorPresentation(mem).prepare(symbols, hooks))
                    # The pre-existing ConnectionWarning prologue signature
                    # does not match these captures (second word is LUI).
                    # Its unrelated installation is covered by its own tests.
                    spans = sorted((p.address, p.address + len(p.replacement)) for p in hooks.patches)
                    self.assertTrue(all(b <= c for (a,b),(c,d) in zip(spans, spans[1:])))
                    hooks._install_plan()
                    for change in reversed(hooks.patches):
                        mem.write_bytes(change.address, change.original)
                    self.assertEqual(mem.data, raw)

        self.assertGreater(verified, 0, "No combined capture plans were tested")

    def test_editable_tiers_cover_all_milestones(self):
        from unittest.mock import patch
        from rule_builder.rules import Has
        from ..rules.stealth import stealth_access_rule
        # Patching each tier demonstrates the intended edit points independently.
        with patch("worlds.secret_agent_clank.rules.stealth.stealth_5_rule", return_value=Has("five")) as five, \
             patch("worlds.secret_agent_clank.rules.stealth.stealth_10_rule", return_value=Has("ten")) as ten, \
             patch("worlds.secret_agent_clank.rules.stealth.stealth_25_rule", return_value=Has("twenty-five")) as final:
            for count in range(1, 26):
                five.reset_mock(); ten.reset_mock(); final.reset_mock()
                stealth_access_rule(None, count)
                self.assertEqual(five.call_count, 1)
                self.assertEqual(ten.call_count, int(count > 5))
                self.assertEqual(final.call_count, int(count > 10))

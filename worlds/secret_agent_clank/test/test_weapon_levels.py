import struct
import unittest

from BaseClasses import CollectionState
from test.general import setup_multiworld

from ..constants import CASE_NAME_TO_INFOBOT, SACCases
from ..constants.weapon_order import WEAPON_ORDER
from ..constants.weapon_progression import (
    LEVELLED_INTERNALS, PROGRESSIVE_TO_INTERNAL, checked_levels, level_location_name, max_level,
)
from ..core.patches.progression import Progression
from ..options import ProgressiveWeapons
from ..world import SecretAgentClankWorld
from .mips_cpu import CPU
from .test_runtime import Memory as ByteMemory


class Memory(ByteMemory):
    def write_bytes(self, address, data):
        self.data[address:address + len(data)] = data

    def write_int32(self, address, value):
        self.batch_write_int32([(address, value)])


class WeaponLevelTests(unittest.TestCase):
    def test_roster_and_caps(self):
        self.assertEqual(len(LEVELLED_INTERNALS), 15)
        self.assertEqual(set(LEVELLED_INTERNALS), set(PROGRESSIVE_TO_INTERNAL.values()))
        for internal in ("superkick", "kicksplosion", "kickblast", "clankpda", "ratchetpda", "bolttransfer"):
            self.assertEqual(max_level(internal, 1), 1)
            self.assertEqual(checked_levels(internal, 4, 1), ())
        self.assertEqual(checked_levels("ryno", 4, 1), (2, 3, 4))
        self.assertEqual(checked_levels("throwTie", 3, 0), (4,))
        self.assertEqual(checked_levels("throwTie", 3, 1), (4, 8))

    def test_old_boolean_is_automatic_and_new_manual_survives_slot_data(self):
        self.assertEqual(ProgressiveWeapons.from_any(True).value, 2)
        self.assertEqual(ProgressiveWeapons.from_any("true").value, 2)
        self.assertEqual(ProgressiveWeapons.from_any("manual").value, 1)
        for mode, manual in ((True, False), (2, False), (1, True)):
            p = Progression(Memory())
            p.configure({"progressive_weapons": mode})
            self.assertTrue(p.enabled)
            self.assertEqual(p.manual, manual)

    def test_generated_modes_and_counts(self):
        from Fill import distribute_items_restrictive
        for mode in ("off", "manual", "automatic"):
            for ng in (0, 1, 2):
                m = setup_multiworld(SecretAgentClankWorld, options={
                    "progressive_weapons": mode, "weapon_level_checks": "all", "ng_plus": ng,
                    "all_missions": "all", "all_cutscenes": True, "skill_points": True,
                })
                checks = m.get_region("Weapon Levels", 1).locations
                self.assertEqual(len(checks), 101 if ng else 42)
                self.assertEqual(len(m.itempool), len(m.get_unfilled_locations(1)))
                slot = m.worlds[1].fill_slot_data()
                self.assertEqual(slot["progressive_weapons"], {"off": 0, "manual": 1, "automatic": 2}[mode])
                self.assertEqual(slot["weapon_level_checks"], 4)
                distribute_items_restrictive(m)
                self.assertTrue(m.fulfills_accessibility())

    def test_tracker_round_trip_and_old_slot_defaults(self):
        from ..universal_tracker import setup_options_from_slot_data
        m = setup_multiworld(SecretAgentClankWorld, options={
            "progressive_weapons": "manual", "weapon_level_checks": "level_4"})
        world = m.worlds[1]
        slot = world.fill_slot_data()
        m.re_gen_passthrough = {world.game: slot}
        world.options.progressive_weapons.value = 0
        world.options.weapon_level_checks.value = 0
        setup_options_from_slot_data(world)
        self.assertEqual(world.options.progressive_weapons.value, 1)
        self.assertEqual(world.options.weapon_level_checks.value, 1)
        slot["progressive_weapons"] = True
        del slot["weapon_level_checks"]
        setup_options_from_slot_data(world)
        self.assertEqual(world.options.progressive_weapons.value, 2)
        self.assertEqual(world.options.weapon_level_checks.value, 0)

    def test_disabled_characters_and_ng_only_checks(self):
        for ng in (0, 1):
            m = setup_multiworld(SecretAgentClankWorld, options={
                "operatives": {"Clank": 1}, "weapon_level_checks": "level_8", "ng_plus": ng})
            checks = m.get_region("Weapon Levels", 1).locations
            self.assertEqual(len(checks), 6 if ng else 0)
            self.assertTrue(all("(Clank)" in loc.name for loc in checks))

    def test_clank_case_mapping_can_be_filled_in(self):
        from unittest.mock import patch
        from ..locations.weapon_levels import CLANK_WEAPON_LEVEL_CASES
        with patch.dict(CLANK_WEAPON_LEVEL_CASES, {"throwTie": (SACCases.VENANTONIO_LABS,)}):
            m = setup_multiworld(SecretAgentClankWorld, options={"weapon_level_checks": "all"})
        world = m.worlds[1]
        state = CollectionState(m)
        state.prog_items[1].clear()
        state.stale[1] = True
        state.collect(world.create_item("Tie-A-Rang (Clank)"), prevent_sweep=True)
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.ASYANICA_ROOFTOPS]), prevent_sweep=True)
        location = m.get_location(level_location_name("throwTie", 2), 1)
        self.assertFalse(location.can_reach(state))
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.VENANTONIO_LABS]), prevent_sweep=True)
        self.assertTrue(location.can_reach(state))

    def test_clank_levels_need_enemy_access(self):
        m = setup_multiworld(SecretAgentClankWorld, options={"weapon_level_checks": "all"})
        world = m.worlds[1]
        state = CollectionState(m)
        state.prog_items[1].clear()
        state.stale[1] = True
        state.collect(world.create_item("Cufflink Bomb (Clank)"), prevent_sweep=True)
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.KLUNKS_LAIR]), prevent_sweep=True)
        location = m.get_location(level_location_name("CuffLink", 2), 1)
        self.assertFalse(location.can_reach(state))
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.BOLTAIRE_MUSEUM]), prevent_sweep=True)
        self.assertTrue(location.can_reach(state))

    def test_case_access_and_required_copies(self):
        for mode in ("off", "manual", "automatic"):
            m = setup_multiworld(SecretAgentClankWorld, options={
                "progressive_weapons": mode, "weapon_level_checks": "all",
                "starting_weapons": 0, "starting_gadgets": 0,
            })
            world = m.worlds[1]
            from ..constants.weapons import EQUIPMENT_INTERNAL_TO_DISPLAY
            for internal, case, wrong_case in (
                ("blaster", SACCases.MAX_SECURITY_CELLS, SACCases.ASYANICA_ROOFTOPS),
                ("throwTie", SACCases.ASYANICA_ROOFTOPS, SACCases.MAX_SECURITY_CELLS),
            ):
                # Construct a state without the randomly precollected starting cases.
                state = CollectionState(m)
                state.prog_items[1].clear()
                state.stale[1] = True
                location = m.get_location(level_location_name(internal, 4), 1)
                item = (next(n for n, i in PROGRESSIVE_TO_INTERNAL.items() if i == internal)
                        if mode != "off" else EQUIPMENT_INTERNAL_TO_DISPLAY[internal])
                for _ in range(3 if mode != "off" else 1):
                    state.collect(world.create_item(item), prevent_sweep=True)
                state.collect(world.create_item(CASE_NAME_TO_INFOBOT[wrong_case]), prevent_sweep=True)
                self.assertFalse(location.can_reach(state))
                state.collect(world.create_item(CASE_NAME_TO_INFOBOT[case]), prevent_sweep=True)
                self.assertEqual(location.can_reach(state), mode == "off")
                if mode != "off":
                    state.collect(world.create_item(item), prevent_sweep=True)
                    self.assertTrue(location.can_reach(state))

    def test_progressive_ownership_is_removed_with_last_copy(self):
        m = setup_multiworld(SecretAgentClankWorld, options={
            "progressive_weapons": "manual", "starting_weapons": 0, "starting_gadgets": 0})
        world = m.worlds[1]
        state = CollectionState(m)
        item = world.create_item("Progressive Tie-A-Rang (Clank)")
        for _ in range(2):
            state.collect(item, prevent_sweep=True)
        state.remove(item)
        self.assertTrue(state.has("Tie-A-Rang (Clank)", 1))
        self.assertEqual(state.count(item.name, 1), 1)
        state.remove(item)
        self.assertFalse(state.has("Tie-A-Rang (Clank)", 1))
        self.assertEqual(state.count(item.name, 1), 0)

    def test_manual_preserves_earned_levels_freezes_xp_and_bridges_ng(self):
        p = Progression(Memory())
        p.configure({"progressive_weapons": 1, "ng_plus": 1, "weapon_level_checks": 4})
        p.base, p.cap_address = 0x100000, 0x120000
        slot = p.base + WEAPON_ORDER.index("blaster") * 0x74
        name = next(n for n, i in PROGRESSIVE_TO_INTERNAL.items() if i == "blaster")
        p.receive([name] * 4)
        p.pine.batch_write_int32([(slot + 0x5C, 1), (slot + 0x64, 50), (slot + 0x70, 1)])
        p.sync()
        self.assertEqual(p.pine.read_int32(slot + 0x5C), 1)
        self.assertEqual(p.pine.read_int32(slot + 0x64), 50)
        self.assertEqual(p.level_checks(), [level_location_name("blaster", 2)])
        p.pine.batch_write_int32([(slot + 0x5C, 3)])
        p.sync()
        self.assertEqual(p.pine.read_int32(slot + 0x5C), 3)
        self.assertEqual(p.pine.read_int32(slot + 0x64), 0)
        p.receive([name] * 5)
        p.sync()
        self.assertEqual(p.pine.read_int32(slot + 0x5C), 4)
        p.receive([name] * 8)
        p.sync()
        self.assertEqual(p.pine.read_int32(slot + 0x5C), 4)
        p.receive([name])
        p.sync()
        self.assertEqual(p.pine.read_int32(slot + 0x5C), 0)

    def test_native_manual_guard_blocks_cap_and_resumes_original(self):
        # Execute actual emitted MIPS, stopping at the original body or caller.
        base, caps, xp, wrapper = 0x100000, 0x120000, 0x130000, 0x140000
        for internal in LEVELLED_INTERNALS:
            slot = WEAPON_ORDER.index(internal)
            for cap, native_level, allowed in ((0, 0, False), (1, 0, False),
                                               (4, 2, True), (4, 3, False), (8, 3, True)):
                memory = Memory()
                memory.write_bytes(caps, bytes([cap] * len(WEAPON_ORDER)))
                memory.batch_write_int32([(base + slot * 0x74 + 0x5C, native_level)])
                original = struct.pack("<2I", 0x27BDFFB0, 0xFFB30028)
                tail, continuation = 0x150000, 0x160000
                from ..core.patches.asm import jump, packed
                memory.write_bytes(tail, original + packed([jump(xp + 8), 0]))
                def allocate(code):
                    memory.write_bytes(continuation, code)
                    return continuation
                memory.write_bytes(wrapper, Progression.manual_xp_guard(base, caps, tail, allocate))
                cpu = CPU(memory)
                cpu.r[29] = 0x700000
                cpu.r[4:7] = [slot, 50, 1]
                cpu.r[19] = 123
                cpu.run(wrapper, stop=xp + 8 if allowed else CPU.STOP)
                self.assertEqual(cpu.r[4:7], [slot, 50, 1])
                if allowed:
                    self.assertEqual(cpu.r[29], 0x700000 - 0x50)
                    self.assertEqual(memory.read_int32(cpu.r[29] + 0x28), 123)
                else:
                    self.assertEqual(cpu.r[29], 0x700000)

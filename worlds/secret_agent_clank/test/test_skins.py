import struct
import unittest
from pathlib import Path

from ..constants.skins import (
    ALL_SKINS_MASK,
    CLANK_SKINS,
    QWARK_SKINS,
    RATCHET_SKINS,
    SKIN_OWNED_OFFSET,
    SKIN_SAVE_OFFSET,
)
from ..core.patches.asm import packed
from ..core.skins import Skins
from ..core.symbols import RuntimeSymbols
from ..options import ClankSkin, QwarkSkin, RatchetSkin
from .bases import SecretAgentClankTestBase
from .mips_cpu import CPU
from .test_runtime import Memory


class SkinMemory(Memory):
    def write_int8(self, address, value):
        self.batch_write_int8([(address, value)])

    def write_int32(self, address, value):
        self.batch_write_int32([(address, value)])

    def write_bytes(self, address, value):
        self.data[address:address + len(value)] = value


class SkinTests(unittest.TestCase):
    def test_retail_disabled_skin_audit(self):
        captures = list((Path(__file__).parents[1] / ".research").glob("*.ram"))
        if not captures:
            self.skipTest("Local retail research captures not present")
        audited = 0
        for capture in captures:
            p = SkinMemory()
            p.data[:] = capture.read_bytes()
            symbols = RuntimeSymbols.parse(p.data[:0x1000000], 0)
            address = symbols.get("IsSkinUnlocked__F12SPHeroSkinId")
            if address is None:
                continue
            # Grant every prerequisite through call stubs, without changing
            # retail control flow. Only deliberately unavailable skins should
            # still return false; story/NG+/code locks are not missing assets.
            words = struct.unpack("<62I", p.read_bytes(address, 0xF8))
            def prerequisite_met(cpu):
                cpu.r[2] = 1
            stubs = {(word & 0x3FFFFFF) << 2: prerequisite_met
                     for word in words if word >> 26 == 3}
            disabled = set()
            for skin in range(1, 26):
                cpu = CPU(p)
                cpu.r[4] = skin
                cpu.run(address, stubs=stubs)
                if not cpu.r[2]:
                    disabled.add(skin)
            with self.subTest(capture=capture.name):
                self.assertEqual(disabled, {7})
            audited += 1
        self.assertGreater(audited, 0, "No retail skin predicates were audited")

    def fixture(self):
        p = SkinMemory()
        skins = Skins(p)
        skins.flags.pointer_address = 0x110000
        p.write_int32(0x110000, 0x200000)
        p.writes.clear()
        return p, skins

    def test_options_cover_every_native_menu_entry(self):
        for option, expected in ((ClankSkin, CLANK_SKINS), (RatchetSkin, RATCHET_SKINS),
                                 (QwarkSkin, QWARK_SKINS)):
            self.assertEqual(option.options, {"in_game": 0, **expected})
            for name, value in expected.items():
                self.assertEqual(option.from_any(name).value, value)

    def test_old_slot_data_unlocks_without_overwriting_selections_or_currency(self):
        p, skins = self.fixture()
        skins.configure({})
        p.write_int32(0x200000 + SKIN_OWNED_OFFSET, 0x80000001)
        p.write_int8(0x200000 + SKIN_SAVE_OFFSET, 9)
        before = bytes(p.data)
        p.writes.clear()
        self.assertTrue(skins.sync())
        self.assertEqual(p.writes, [(0x200000 + SKIN_OWNED_OFFSET, ALL_SKINS_MASK | 0x80000001)])
        offset = 0x200000 + SKIN_OWNED_OFFSET
        self.assertEqual(p.data[:offset], before[:offset])
        self.assertEqual(p.data[offset + 4:], before[offset + 4:])
        p.writes.clear()
        skins.sync()
        self.assertEqual(p.writes, [])

    def test_all_choices_and_matching_giant_qwark(self):
        for character, values, offset in (("ratchet", RATCHET_SKINS, 0),
                                         ("clank", CLANK_SKINS, 0x34),
                                         ("qwark", QWARK_SKINS, 0x68)):
            for value in values.values():
                p, skins = self.fixture()
                skins.configure({f"{character}_skin": value})
                skins.sync()
                self.assertEqual(p.read_int8(0x200000 + SKIN_SAVE_OFFSET + offset), value)
                if character == "qwark":
                    self.assertEqual(p.read_int8(0x200000 + SKIN_SAVE_OFFSET + 0x9C), value + 4)

    def test_invalid_choices_and_save_pointers_do_not_write(self):
        p, skins = self.fixture()
        for data in ({"clank_skin": 1}, {"ratchet_skin": 11}, {"qwark_skin": 25}):
            with self.assertRaises(ValueError):
                skins.configure(data)
        for base in (0, 0xFFFFFFFF, 0x1FFFFFF):
            p.write_int32(0x110000, base)
            p.writes.clear()
            self.assertFalse(skins.sync())
            self.assertEqual(p.writes, [])

    def test_menu_selection_survives_sync_and_client_restart(self):
        p, skins = self.fixture()
        skins.configure({"clank_skin": 17})
        skins.sync()
        slot = 0x200000 + SKIN_SAVE_OFFSET + 0x34
        for choice in (12, 0):
            p.write_int8(slot, choice)
            skins.sync()
            self.assertEqual(p.read_int8(slot), choice)
            skins = Skins(p)
            skins.flags.pointer_address = 0x110000
            skins.configure({"clank_skin": 17})
            skins.sync()
            self.assertEqual(p.read_int8(slot), choice)

    def test_legacy_robo_ratchet_slot_data_uses_prison_scrubs(self):
        p, skins = self.fixture()
        skins.configure({"ratchet_skin": 7})
        skins.sync()
        self.assertEqual(p.read_int8(0x200000 + SKIN_SAVE_OFFSET), 1)
        self.assertNotIn("robo_ratchet", RatchetSkin.options)
        self.assertEqual(ALL_SKINS_MASK & (1 << 7), 0)

    def test_sync_repairs_robo_ratchet_even_on_initialized_saves(self):
        p, skins = self.fixture()
        p.write_int32(0x200000 + SKIN_OWNED_OFFSET, 0xFFFFFFFE)
        p.write_int8(0x200000 + SKIN_SAVE_OFFSET, 7)
        p.writes.clear()
        skins.sync()
        self.assertEqual(p.writes, [(0x200000 + SKIN_SAVE_OFFSET, 1)])

    def test_native_predicate_hides_only_unsupported_robo_ratchet(self):
        p, skins, symbols = self.native_fixture()
        for edit in skins.prepare(symbols):
            p.write_bytes(edit.address, edit.replacement)
        for skin in range(1, 26):
            cpu = CPU(p)
            cpu.r[4] = skin
            cpu.run(symbols["IsSkinUnlocked__F12SPHeroSkinId"])
            self.assertEqual(cpu.r[2], int(skin != 7))

    def test_native_loader_repairs_robo_ratchet_before_model_swap(self):
        for owned in (0, 0xFFFFFFFE):
            p, skins, symbols = self.native_fixture()
            for edit in skins.prepare(symbols):
                p.write_bytes(edit.address, edit.replacement)
            p.write_int32(0x200000 + SKIN_OWNED_OFFSET, owned)
            p.write_int8(0x200000 + SKIN_SAVE_OFFSET, 7)
            cpu = CPU(p)
            cpu.r[3] = 0x200000 + SKIN_SAVE_OFFSET - 0x1900
            cpu.run(0x123038, stop=0x123040)
            self.assertEqual(cpu.r[3], 1)
            self.assertEqual(p.read_int8(0x200000 + SKIN_SAVE_OFFSET), 1)

    def native_fixture(self):
        p, skins = self.fixture()
        symbols = {"GLOBAL_GetFlag__FUiUc": 0x120000,
                   "SelectedSPHeroSkinID__F8PLR_TYPE": 0x121000,
                   "IsSkinUnlocked__F12SPHeroSkinId": 0x122000,
                   "HEROSKIN_LoadSelectedSpecilaSkin__Fv": 0x123000}
        p.write_bytes(0x120000, packed([0x3C020011, 0x30A500FF, 0x8C430000,
                                       0x00641821, 0x906204E0, 0x03E00008, 0x00451024]))
        p.write_bytes(0x121000, packed([0x0080302D, 0x24050034, 0x00C52818,
                                       0x3C040011, 0x8C830000, 0x3C020001, 0x34428000,
                                       0x00651821, 0x00621821, 0x80621900, 0x14400018]))
        p.write_bytes(0x122000, packed([0x27BDFFF0, 0x2483FFFE, 0xFFB00000, 0x2C620012]))
        p.write_bytes(0x1220E4, packed([0xDFB00000, 0xDFBF0008, 0x03E00008, 0x27BD0010]))
        p.write_bytes(0x12300C, packed([0x3C020011, 0x8C66F990, 0x24070034, 0x8C430000,
                                       0x3C040001, 0x8CC50574, 0x34848000, 0x8CA20044,
                                       0x00471018, 0x00621821, 0x00641821,
                                       0x80631900, 0x10600003]))
        return p, skins, symbols

    def test_native_first_load_applies_all_choices_without_host_sync(self):
        for chosen in ({}, {"ratchet_skin": 3, "clank_skin": 14, "qwark_skin": 20}):
            p, skins, symbols = self.native_fixture()
            skins.configure(chosen)
            before = bytes(p.data)
            edits = skins.prepare(symbols)
            self.assertEqual(p.data, before)
            for edit in edits:
                p.write_bytes(edit.address, edit.replacement)
            # The save can be created/relocated after preparation.
            p.write_int32(0x110000, 0x300000)
            for player_type in range(4):
                cpu = CPU(p)
                cpu.r[3] = 0x300000 + 0x18000 + player_type * 0x34
                expected = (3, 14, 20, 24)[player_type] if chosen else 0
                cpu.run(0x123038, stop=0x123040 if expected else 0x12304C)
                self.assertEqual(cpu.r[3], expected)
                self.assertEqual(p.read_int32(0x300000 + SKIN_OWNED_OFFSET), ALL_SKINS_MASK)
            for edit in reversed(edits):
                p.write_bytes(edit.address, edit.original)
            self.assertEqual(p.data[0x120000:0x124000], before[0x120000:0x124000])

    def test_unknown_native_layout_is_rejected_without_writes(self):
        for address in (0x120000, 0x121014, 0x122000, 0x1220E4, 0x12301C, 0x123038):
            p, skins, symbols = self.native_fixture()
            p.data[address] ^= 1
            before = bytes(p.data)
            with self.assertRaises(RuntimeError):
                skins.prepare(symbols)
            self.assertEqual(p.data, before)

    def test_native_loader_preserves_menu_selection_after_initialization(self):
        p, skins, symbols = self.native_fixture()
        skins.configure({"clank_skin": 17})
        skins.sync()
        for edit in skins.prepare(symbols):
            p.write_bytes(edit.address, edit.replacement)
        slot = 0x200000 + SKIN_SAVE_OFFSET + 0x34
        for choice in (12, 0):
            p.write_int8(slot, choice)
            cpu = CPU(p)
            cpu.r[3] = slot - 0x1900
            cpu.run(0x123038, stop=0x123040 if choice else 0x12304C)
            self.assertEqual(cpu.r[3], choice)
            self.assertEqual(p.read_int8(slot), choice)

    def test_captured_native_loader_initializes_before_model_swap(self):
        captures = list((Path(__file__).parents[1] / ".research").glob("*.ram"))
        if not captures:
            self.skipTest("Local research captures not present")
        for capture in captures:
            p = SkinMemory()
            p.data[:] = capture.read_bytes()
            symbols = RuntimeSymbols.parse(p.data[:0x1000000], 0)
            if "IsSkinUnlocked__F12SPHeroSkinId" not in symbols:
                continue
            # Retail explicitly hides ID 7; AP must not expose unavailable
            # assets simply because their names exist in the menu tables.
            cpu = CPU(p)
            cpu.r[4] = 7
            cpu.run(symbols["IsSkinUnlocked__F12SPHeroSkinId"])
            self.assertEqual(cpu.r[2], 0)
            for selected in ({}, {"ratchet_skin": 10, "clank_skin": 17, "qwark_skin": 21}):
                with self.subTest(capture=capture.name, selected=selected):
                    p.data[:] = capture.read_bytes()
                    skins = Skins(p)
                    skins.configure(selected)
                    edits = skins.prepare(symbols)
                    for edit in edits:
                        p.write_bytes(edit.address, edit.replacement)
                    base = p.read_int32(skins.flags.pointer_address)
                    p.write_int32(base + SKIN_OWNED_OFFSET, 0x80000000)
                    for player_type in range(4):
                        p.write_int8(base + SKIN_SAVE_OFFSET + player_type * 0x34, 0)
                    for player_type in range(4):
                        slot = base + SKIN_SAVE_OFFSET + player_type * 0x34
                        cpu = CPU(p)
                        cpu.r[3] = slot - 0x1900
                        load = symbols["HEROSKIN_LoadSelectedSpecilaSkin__Fv"]
                        expected = (10, 17, 21, 25)[player_type] if selected else 0
                        cpu.run(load + 0x38, stop=load + (0x40 if expected else 0x4C))
                        self.assertEqual(cpu.r[3], expected)
                        self.assertEqual(p.read_int32(base + SKIN_OWNED_OFFSET), ALL_SKINS_MASK | 0x80000000)
                        self.assertEqual(cpu.r[31], CPU.STOP)
                    cpu = CPU(p)
                    cpu.run(symbols["IsSkinUnlocked__F12SPHeroSkinId"])
                    self.assertEqual(cpu.r[2], 1)


class SkinGenerationTests(SecretAgentClankTestBase):
    options = {"clank_skin": "zoni", "ratchet_skin": "dan", "qwark_skin": "lucha_libre_qwark"}

    def test_slot_data_contains_cosmetic_choices(self):
        data = self.multiworld.worlds[1].fill_slot_data()
        self.assertEqual((data["clank_skin"], data["ratchet_skin"], data["qwark_skin"]), (17, 10, 21))

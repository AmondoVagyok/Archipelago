"""Use AP ownership at the Treehouse door without writing pickup save bits."""
from ...constants import KEYCARD_ITEMS
from ..global_flags import GlobalFlags
from ..symbols import require
from . import mips as m
from ..batch_io import read_blocks
from .asm import Patch, capture, jump, packed, words
from .gain_storage import GainStorage
from .storage import plan_storage


class KeycardHunt:
    def __init__(self, pine):
        self.pine = pine
        self.enabled = False
        self.mask = 0
        self.table = self.entry = self.pointer_address = None
        self.code = b""

    def receive(self, names):
        self.mask = sum(1 << bit for name, bit in KEYCARD_ITEMS.items() if name in names)

    @staticmethod
    def routine(table, getter, original):
        # Only flag AA is redirected. Other flags execute the original getter.
        # Use only registers the original leaf function already clobbers.
        return packed([
            m.addiu(m.V0, m.ZERO, 0xAA), m.bne(m.A0, m.V0, 6),
            m.andi(m.A1, m.A1, 0xFF), *m.li32(m.V0, table),
            m.lbu(m.V0, 0, m.V0), m.jr(m.RA), m.and_(m.V0, m.V0, m.A1),
            words(original)[0], jump(getter + 8), words(original)[1],
        ])

    def prepare(self, symbols, hooks, module):
        self.table = self.entry = self.pointer_address = None
        if not self.enabled or module != 31:
            return []
        flags = GlobalFlags(self.pine)
        if not flags.bind(symbols):
            raise RuntimeError("Keycard Hunt flag getter layout changed")
        getter = require(symbols, "GLOBAL_GetFlag__FUiUc")
        original = self.pine.read_bytes(getter, 8)
        ranges = list(hooks.extra_ranges)
        edits = []
        sizes = [44, 4]
        addresses = plan_storage(ranges, hooks.patches, sizes)
        if addresses is None and not hooks.gain_storage_prepared:
            guards, extra = GainStorage(self.pine).prepare(symbols)
            edits.extend(guards)
            ranges.extend(extra)
            hooks.extra_ranges.extend(extra)
            hooks.gain_storage_prepared = True
            addresses = plan_storage(ranges, hooks.patches + edits, sizes)
        if addresses is None:
            raise RuntimeError("Insufficient verified storage for Keycard Hunt")
        entry, table = addresses
        code = self.routine(table, getter, original)
        edits.extend(capture(self.pine, [(entry, code), (table, packed([self.mask]))]))
        edits.append(Patch(getter, original, packed([jump(entry), m.NOP])))
        self.entry, self.table, self.code = entry, table, code
        self.pointer_address = flags.pointer_address
        return edits

    def sync(self):
        if not self.enabled or self.table is None:
            return
        module, loading, code = read_blocks(self.pine, [(0x206328, 4), (0x206324, 4), (self.entry, len(self.code))])
        if module != packed([31]) or loading != packed([0xFFFFFFFF]):
            return
        if code != self.code:
            raise RuntimeError("Keycard Hunt code changed")
        self.pine.write_int32(self.table, self.mask)

"""Count the successful End(StealthTakeDown) path, not the transient enemy list."""
import struct
from ..constants.stealth import stealth_thresholds, stealth_location_name
from .patches.asm import Patch, jump, packed
from .patches import mips as m

END = "End__15StealthTakeDown"
KILL = "CLANKSTEALTH_GiveStealthKill__FP4Mobyf"


class StealthState:
    def __init__(self, pine):
        self.pine = pine
        self.mode = 0
        self.count = 0
        self.loaded = False
        self.binding = None
        self.on_count = lambda count: None

    def configure(self, mode, *, reset=False):
        stealth_thresholds(mode)
        self.mode = mode
        self.loaded = False
        if reset:
            self.count = 0
            self.binding = None

    def load(self, count):
        if type(count) is not int or not 0 <= count <= 25:
            raise ValueError("Invalid stored stealth count")
        self.count = max(self.count, count)
        self.loaded = True

    @staticmethod
    def wrapper(counter, target):
        # At this call site all these registers are caller-saved; preserve
        # a0, f12 and ra for the original native call via a tail jump.
        return packed([m.lui(m.T0, (counter + 0x8000) >> 16), m.lw(m.T1, counter & 65535, m.T0),
                       m.sltiu(m.T2, m.T1, 25), m.beq(m.T2, m.ZERO, 2),
                       m.addiu(m.T1, m.T1, 1), m.sw(m.T1, counter & 65535, m.T0),
                       jump(target), 0])

    def prepare(self, symbols, allocate):
        self.binding = None
        if not self.mode:
            return []
        end, kill = symbols.get(END), symbols.get(KILL)
        if end is None and kill is None:
            return []  # Modules without Clank's takedown implementation.
        if end is None or kill is None:
            raise RuntimeError("Incomplete native stealth exports")
        # Both failure flags bypass the success-only call at End + 0xB0.
        expected = {0x3C: 0x92220015, 0x40: 0x54400005,
                    0x48: 0x9222002C, 0x4C: 0x10400014,
                    0x98: 0x10000012, 0xA8: 0x3C013F80,
                    0xAC: 0x44816000, 0xB0: jump(kill, link=True),
                    0xB4: 0x8E040010}
        if any(self.pine.read_int32(end + offset) != word for offset, word in expected.items()):
            raise RuntimeError("Native successful stealth takedown path changed")
        counter = allocate(struct.pack("<I", self.count))
        code = self.wrapper(counter, kill)
        address = allocate(code)
        site = end + 0xB0
        original = packed([expected[0xB0]])
        replacement = packed([jump(address, link=True)])
        self.binding = (counter, site, replacement, address, code)
        return [Patch(site, original, replacement)]

    def poll(self):
        if not self.mode or not self.loaded or self.binding is None:
            return
        counter, site, replacement, address, code = self.binding
        # Safe even during loading: never interpret a replaced module as a
        # counter. Poll before the loader installs the next module's plan.
        if (self.pine.read_bytes(site, 4) != replacement
                or self.pine.read_bytes(address, len(code)) != code):
            self.binding = None
            return
        count = self.pine.read_int32(counter)
        if not 0 <= count <= 25:
            raise RuntimeError("Invalid native stealth count")
        if count > self.count:
            self.count = count
            self.on_count(count)
        elif count < self.count:
            # Restore server progress after a reload/savestate rollback.
            self.pine.batch_write_int32([(counter, self.count)])

    def checks(self):
        if not self.loaded:
            return ()
        return tuple(stealth_location_name(n) for n in stealth_thresholds(self.mode)
                     if n <= self.count)

"""Latch the native Mission Failed text renderer until the module reloads."""
from .patches import Patch, jump, mips as m, packed


class MissionFailure:
    def __init__(self, pine):
        self.pine = pine
        self.binding = None

    def prepare(self, symbols, allocate):
        self.binding = None
        render = symbols.get("CLANK_MissionFailedText__FPv")
        if render is None:
            return []
        get_string = symbols.get("GetStr__Fi")
        site = render + 0x14
        if (get_string is None or self.pine.read_bytes(site, 8)
                != packed([jump(get_string, True), m.addiu(m.A0, m.ZERO, 934)])):
            raise RuntimeError("Native Mission Failed renderer changed")
        original = packed([jump(get_string, True)])
        flag = allocate(packed([0]))
        # Record this call's return address as the latch, then tail-call
        # GetStr with its original arguments/RA. Only caller-saved t0 changes.
        code = packed([m.lui(m.T0, (flag + 0x8000) >> 16),
                       jump(get_string), m.sw(m.RA, flag & 0xFFFF, m.T0)])
        entry = allocate(code)
        replacement = packed([jump(entry, True)])
        self.binding = site, replacement, entry, code, flag
        return [Patch(site, original, replacement)]

    def active(self):
        if self.binding is None:
            return False
        site, replacement, entry, code, flag = self.binding
        if (self.pine.read_bytes(site, 4) != replacement
                or self.pine.read_bytes(entry, len(code)) != code):
            return False
        return self.pine.read_int32(flag) == site + 8

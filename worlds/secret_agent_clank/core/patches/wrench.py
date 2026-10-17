"""Ratchet-only wrench input gates and progressive native mod entitlements."""
import struct

from ...constants import NativeFunctions
from ..symbols import require
from ..batch_io import read_blocks
from .asm import Patch
from .patch import PatchSet

PROGRESSIVE_WRENCH = "Progressive Wrench"
WRENCH_MODS = ("wrenchpower_firebomb", "wrenchpower_triplewave",
              "wrenchpower_crystallix", "wrenchpower_wildburst")
RATCHET_MODULES = {3, 9, 14, 21, 25}


class WrenchProgression(PatchSet):
    def __init__(self, pine):
        super().__init__(pine)
        self.enabled = False
        self.count = 0
        self.module = None
        self.sites = []
        self.power_address = None

    def entitlements(self):
        return {name: self.count >= index + 2 for index, name in enumerate(WRENCH_MODS)} if self.enabled else {}

    def prepare(self, symbols, module):
        self.patches = []
        self.module, self.sites = module, []
        self.power_address = None
        if not self.enabled or module not in RATCHET_MODULES:
            return []
        # These masks consume only the wrench button. Gun, movement, jump,
        # and camera masks are untouched. Resolve each Ratchet-only export.
        specs = (
            (NativeFunctions.RATCHET_UPDATE_CONTROLS_NORMAL_ACTION_BUTTONS, 0x538, 0x27BDFFC0, 0x30A20020, 2),
            (NativeFunctions.RATCHET_UPDATE_CONTROLS_CROUCH_ACTION_BUTTONS, 0x228, 0x27BDFFE0, 0x30420020, 1),
            (NativeFunctions.RATCHET_CHECK_JUMP_ATTACK, 0x158, 0x27BDFFE0, 0x30420020, 1),
        )
        addresses = [require(symbols, name) for name, *_ in specs]
        blocks = read_blocks(self.pine, [(address, size) for address, (_, size, *_) in zip(addresses, specs)])
        for address, block, (name, size, prologue, mask, expected) in zip(addresses, blocks, specs):
            code = struct.unpack("<" + "I" * (size // 4), block)
            if code[0] != prologue:
                raise RuntimeError(f"Unrecognized Ratchet wrench gate: {name}")
            sites = [(address + i * 4, word) for i, word in enumerate(code) if word == mask]
            if len(sites) != expected:
                raise RuntimeError(f"Ratchet wrench input layout changed: {name}")
            self.sites.extend(sites)
        self.power_address = require(symbols, "g_wrench_wrenchPower")
        self.patches = [Patch(a, struct.pack("<I", word), struct.pack("<I", word if self.count else word & 0xFFFF0000))
                for a, word in self.sites]
        return self.patches

    def sync(self):
        if not self.enabled or not self.sites:
            return
        power = (self.power_address,) if self.power_address is not None else ()
        module, loading, *current = self.pine.batch_read_int32(
            [0x206328, 0x206324, *power, *(address for address, _ in self.sites)])
        if module != self.module or loading != 0xFFFFFFFF:
            return
        writes = []
        # Previously selected vanilla mods must not bypass AP ownership.
        if power:
            selected = current.pop(0)
            if selected > max(0, self.count - 1):
                writes.append((self.power_address, 0))
        for (address, original), word in zip(self.sites, current):
            if word not in (original, original & 0xFFFF0000):
                raise RuntimeError("Wrench gate changed; refusing an unknown code write")
            # Each write changes only an ANDI immediate in one aligned word.
            # Both versions are valid independently, including in a delay slot.
            desired = original if self.count else original & 0xFFFF0000
            if word != desired:
                writes.append((address, desired))
        if writes:
            self.pine.batch_write_int32(writes)

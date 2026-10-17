"""Temporary replacement of the verified 32x32 Shock Rocket icon."""
import struct

from ..symbols import require
from ..vendor import VendorState
from ..batch_io import read_blocks, write_blocks
from .asm import capture
from .patch import PatchSet


class VendorIconPreview(PatchSet):
    ICON_ID = 73
    IMAGE_SIZE = 1024
    PALETTE_SIZE = 1024

    def __init__(self, pine):
        super().__init__(pine)
        self.vendor = VendorState(pine)
        self.module = self.texture_slot = self.texture = self.cache = None
        self.installed = False

    def prepare(self, symbols, *, indices, palette, selected_only=True):
        if self.installed:
            raise RuntimeError("Restore the previous icon test first")
        self.patches = []
        if len(indices) != self.IMAGE_SIZE or len(palette) != self.PALETTE_SIZE:
            raise ValueError("Icon requires 1024 index bytes and 1024 palette bytes")
        if not self.vendor.bind_runtime(symbols) or not self.vendor.active:
            raise RuntimeError("Open a vendor with the SAC client closed")
        row = self.vendor.selected_item()
        if selected_only and (row is None or row.icon != self.ICON_ID):
            raise RuntimeError("Highlight Shock Rocket for the verified icon test")
        lookup, invalidate = require(symbols, "GetIconTextureID__14DrawObjManagerUi",
                                     "aglPs2VramInvalidate__Fv")
        module, lookup_code, invalidate_code = read_blocks(self.pine, [(0x206328, 4), (lookup, 24), (invalidate, 12)])
        self.module, = struct.unpack("<I", module)
        w = struct.unpack("<6I", lookup_code)
        if (w[0] & 0xFFFF0000 != 0x3C030000 or w[1] != 0x000420C0
                or w[2] & 0xFFFF0000 != 0x24630000
                or w[3:] != (0x00641821, 0x03E00008, 0x8C620004)):
            raise RuntimeError("Native icon lookup changed")
        low = w[2] & 65535
        table = ((w[0] & 65535) << 16) + (low-65536 if low & 32768 else low)
        self.texture_slot = table + self.ICON_ID*8 + 4
        self.texture = self.pine.read_int32(self.texture_slot)
        if not 0x100000 <= self.texture < 0x1FFFF00:
            raise RuntimeError("Invalid icon texture object")
        data = self.pine.read_bytes(self.texture, 0xA8)
        if (data[0x10:0x30].split(b"\0", 1)[0] != b"weapon_shockrocket.tga"
                or struct.unpack_from("<I", data, 0x34)[0] != 0x00200020
                or struct.unpack_from("<I", data, 0x64)[0] != 0x93010020
                or struct.unpack_from("<I", data, 0xA4)[0] != 0x80000010):
            raise RuntimeError("Shock Rocket texture format changed")
        image = struct.unpack_from("<I", data, 0x58)[0]
        clut = struct.unpack_from("<I", data, 0x98)[0]
        if not 0x100000 <= image < 0x1FFF800 or clut != image+1024:
            raise RuntimeError("Native icon pixel allocation changed")
        w = struct.unpack("<3I", invalidate_code)
        if w[0] & 0xFFFF0000 != 0x3C020000 or w[1] != 0x03E00008 or w[2] & 0xFFFF0000 != 0xAC400000:
            raise RuntimeError("VRAM invalidation routine changed")
        low = w[2] & 65535
        self.cache = ((w[0] & 65535) << 16) + (low-65536 if low & 32768 else low)
        self.patches = capture(self.pine, [(image, bytes(indices)), (clut, bytes(palette))])
        return self.patches

    def _check_context(self):
        if (self.pine.get_game_id() != "SCUS-97623"
                or self.pine.batch_read_int32([0x206328, 0x206324, self.texture_slot])
                != [self.module, 0xFFFFFFFF, self.texture]):
            raise RuntimeError("Icon preview context changed")

    def apply(self):
        self._check_context()
        if self.installed:
            raise RuntimeError("Icon preview already installed")
        super().apply()
        self.installed = True
        self.pine.write_int32(self.cache, 0)

    def restore(self):
        if not self.installed:
            return
        self._check_context()
        spans = [(patch.address, len(patch.replacement)) for patch in self.patches]
        if read_blocks(self.pine, spans) != [patch.replacement for patch in self.patches]:
            raise RuntimeError("Icon pixels changed; refusing stale restoration")
        write_blocks(self.pine, [*((patch.address, patch.original) for patch in reversed(self.patches)),
                                 (self.cache, bytes(4))])
        if read_blocks(self.pine, spans) != [patch.original for patch in self.patches]:
            raise RuntimeError("Icon restoration failed")
        self.installed = False

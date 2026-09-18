"""Hold the resident MCP loop after relocation and before level-thread startup."""
from .asm import packed, branch


class LoaderGate:
    SITE = 0x01E66414
    ORIGINAL = 0x24040005
    HELD = branch(SITE, 0x01E66A60)
    SIGNATURE_START = 0x01E66400
    SIGNATURE = (
        0x0C7993A8, 0, 0x2405FFFF, 0x10450194, 0x3C0201F5,
        ORIGINAL, 0x2442A740, 0xAE24DAB8, 0x24030001,
        0xAC450004, 0x0C799CE0, 0xAC430018,
    )
    STATE = 0x01EDDAB8
    HANDLE = 0x01EDC7D0
    TARGET = 0x01EDDAE4
    LOAD_THREAD = 0x01EDDAE8
    MODULES = 0x01FBE750

    def __init__(self, pine):
        self.pine = pine
        self.armed = False

    def validate(self, *, patched=False):
        if self.pine.get_game_id() != "SCUS-97615":
            raise RuntimeError("Loader gate requires SCUS-97615")
        expected = list(self.SIGNATURE)
        if patched:
            expected[5] = self.HELD
        if self.pine.read_bytes(self.SIGNATURE_START, len(expected) * 4) != packed(*expected):
            raise RuntimeError("Resident loader signature changed")

    def arm(self):
        self.validate(patched=self.armed)
        if not self.armed:
            self.armed = True  # allows recovery after an uncertain write
            self.pine.write_int32(self.SITE, self.HELD)
            self.validate(patched=True)

    def held_module(self):
        if not self.armed:
            return None
        self.validate(patched=True)
        p = self.pine
        before = (p.read_int32(self.STATE), p.read_int32(self.LOAD_THREAD))
        handle, target = p.read_int32(self.HANDLE), p.read_int32(self.TARGET)
        if before != (4, 0) or not 0 <= handle < 8 or not 0 <= target <= 24:
            return None
        entry = self.MODULES + handle * 0x418
        base, flags = p.read_int32(entry + 4), p.read_int32(entry + 8)
        if not flags & 1 or not 0x100000 <= base < 0x1E00000:
            return None
        if before != (p.read_int32(self.STATE), p.read_int32(self.LOAD_THREAD)):
            return None
        return target, base

    def release(self):
        if not self.armed:
            return
        self.validate(patched=True)
        self.pine.write_int32(self.SITE, self.ORIGINAL)
        self.validate()
        self.armed = False

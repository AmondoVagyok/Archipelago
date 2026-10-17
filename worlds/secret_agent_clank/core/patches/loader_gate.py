"""Research barrier between DLL relocation and starting the level thread."""
import struct


class LoaderBarrierLost(RuntimeError):
    """The complete original loader returned while our barrier was armed."""


class LoaderGate:
    SITE = 0x103BCC
    ORIGINAL = 0x24030005
    HELD = 0x10000069  # beq zero, zero, 0x103D74; existing delay slot is safe
    STATE = 0x1AAE3C
    STATUS = 0x19EF04
    TARGET = 0x1AAE78
    HANDLE = 0x1AAE5C
    SIGNATURE_START = 0x103BB8
    SIGNATURE = (0x0C0400A6, 0, 0x2404FFFF, 0x1044006B, 0x3C020020,
                 ORIGINAL, 0x24426320, 0xAE43AE3C, 0xAC510018,
                 0x0C04107A, 0xAC440004)

    def __init__(self, pine):
        self.pine = pine
        self.armed = False
        self._held_candidate = None

    def validate(self, *, patched=False):
        if self.pine.get_game_id() != "SCUS-97623":
            raise RuntimeError("Loader barrier supports only SCUS-97623")
        expected = list(self.SIGNATURE)
        if patched:
            expected[5] = self.HELD
        actual = self.pine.read_bytes(self.SIGNATURE_START, len(expected) * 4)
        if actual != struct.pack("<11I", *expected):
            if len(actual) != len(expected) * 4:
                detail = f"short read: expected {len(expected) * 4} bytes, got {len(actual)}"
            else:
                words = struct.unpack("<11I", actual)
                detail = "; ".join(
                    f"0x{self.SIGNATURE_START + index * 4:08X}: "
                    f"expected 0x{wanted:08X}, got 0x{found:08X}"
                    for index, (wanted, found) in enumerate(zip(expected, words))
                    if wanted != found)
                if patched and words == self.SIGNATURE:
                    detail += ("; loader barrier was restored to original game code "
                               "while this client still considered it armed "
                               "(possible game reset, save-state load, or another client)")
                    raise LoaderBarrierLost(f"Resident loader signature changed ({detail})")
            raise RuntimeError(f"Resident loader signature changed ({detail})")

    def arm(self):
        if self.armed:
            raise RuntimeError("Loader barrier already armed")
        self.validate()
        # Mark before the write so finally can recover a failed readback.
        self.armed = True
        self._held_candidate = None
        self.pine.write_int32(self.SITE, self.HELD)
        self.validate(patched=True)

    def held_module(self, *, settled=False):
        if not self.armed:
            self._held_candidate = None
            return None
        self.validate(patched=True)
        p = self.pine
        addresses = [self.STATE, self.STATUS, self.TARGET, self.HANDLE]
        before = tuple(p.batch_read_int32(addresses))
        after = tuple(p.batch_read_int32(addresses))
        state, status, target, handle = before
        # State 4 + completed relocation. State 5 can still display a loading
        # screen but the level thread is already running and is NOT safe.
        if before != after or (state, status) != (4, 1) or not 0 <= target < 33 or not handle:
            self._held_candidate = None
            return None
        if settled:
            # NativeRuntime calls once per poll. Do not scan or patch the DLL
            # on the first observation of completed relocation; the entire
            # loader identity must remain held through the next poll.
            previous, self._held_candidate = self._held_candidate, before
            if previous != before:
                return None
        elif self._held_candidate is not None and self._held_candidate != before:
            self._held_candidate = None
            return None
        return target

    def release(self):
        if not self.armed:
            return
        if self.pine.get_game_id() != "SCUS-97623":
            raise RuntimeError("Game changed; refusing resident code restoration")
        word = self.pine.read_int32(self.SITE)
        if word == self.HELD:
            self.validate(patched=True)
            self.pine.write_int32(self.SITE, self.ORIGINAL)
        elif word != self.ORIGINAL:
            raise RuntimeError("Barrier was replaced; refusing to overwrite unknown code")
        self.validate()
        self.armed = False
        self._held_candidate = None

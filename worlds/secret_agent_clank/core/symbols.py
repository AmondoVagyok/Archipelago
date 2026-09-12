"""Resolve the USA SNR2 module's resident exports without executing game code.

Records are {tag, name_pointer, value}, three little-endian words. Reading
name_pointer - 8 returns the PREVIOUS export's value, which can look plausible
while identifying an unrelated function. Verified against GetCurrentPauseScreen,
GADGET_GetData, and WeaponPickup_GiveWeapon in a live Boltaire Museum dump.
"""
import struct


class RuntimeSymbols:
    def __init__(self, pine):
        self.pine = pine
        self.values: dict[str, int] = {}

    def clear(self) -> None:
        self.values.clear()

    def refresh(self) -> None:
        self.clear()
        start, end = 0x600000, 0x1000000
        data = b"".join(self.pine.read_bytes(a, min(0x20000, end - a))
                        for a in range(start, end, 0x20000))
        self.values = self.parse(data, start)

    @staticmethod
    def parse(data: bytes, start: int) -> dict[str, int]:
        result: dict[str, int] = {}
        ambiguous: set[str] = set()
        for offset in range(0, len(data) - 11, 4):
            tag, pointer, value = struct.unpack_from("<III", data, offset)
            if tag >> 16 not in (0x102, 0x103):
                continue
            index = pointer - start
            if not 0 <= index < len(data) or not 0x100000 <= value < 0x2000000:
                continue
            end = data.find(b"\0", index, index + 256)
            if end < 0:
                continue
            name = data[index:end]
            if not name or any(c < 33 or c > 126 for c in name):
                continue
            name = name.decode("ascii")
            if name in result and result[name] != value:
                ambiguous.add(name)
            result[name] = value
        return {name: value for name, value in result.items() if name not in ambiguous}

    def get(self, name: str) -> int | None:
        return self.values.get(name)

"""Verified storage in retail debug-print stubs that already do nothing.

These void functions only spill arguments below SP and return. Replacing that
with JR RA/NOP preserves their observable behavior. Their unreachable bodies
can then hold hooks without removing combat XP or assuming unused RAM.
"""
from .location_hooks import Patch, packed


def prepare_gain_storage(pine, symbols):
    text = [0x27BDFF90, 0xFFA70048, 0xFFA80050, 0xFFA90058,
            0xFFAA0060, 0xFFAB0068, 0xE7AC0038, 0xE7AE003C,
            0xE7B00040, 0xE7B20044, 0x03E00008, 0x27BD0070]
    vector = [0x27BDFF90, 0xFFA60040, 0xFFA70048, 0xFFA80050,
              0xFFA90058, 0xFFAA0060, 0xFFAB0068, 0xE7AC0030,
              0xE7AE0034, 0xE7B00038, 0xE7B2003C, 0x03E00008, 0x27BD0070]
    styled = [0x27BDFFA0, 0xFFA80040, 0xFFA90048, 0xFFAA0050,
              0xFFAB0058, 0xE7AC0030, 0xE7AE0034, 0xE7B00038,
              0xE7B2003C, 0x03E00008, 0x27BD0060]
    edits, ranges = [], []
    for name, words in (
            ('DEBUGDRAW_PrintText__FiiUie', text),
            ('DEBUGDRAW_PrintText__FPC4VEC3Uie', vector),
            ('DEBUGDRAW_PrintDropText__FiiUiUie', styled),
            ('DEBUGDRAW_PrintOutlineText__FiiUiUie', styled)):
        address = symbols.get(name)
        expected = packed(words)
        if address is None or pine.read_bytes(address, len(expected)) != expected:
            raise RuntimeError(f'Gain storage stub layout changed: {name}')
        edits.append(Patch(address, expected[:8], packed([0x03E00008, 0])))
        ranges.append((address + 8, address + len(expected)))
    if any(max(a, c) < min(b, d) for i, (a, b) in enumerate(ranges)
           for c, d in ranges[i + 1:]):
        raise RuntimeError('Gain storage stubs overlap')
    return edits, ranges

"""Verified storage in retail debug-print stubs that already do nothing.

These void functions only spill arguments below SP and return. Replacing that
with JR RA/NOP preserves their observable behavior. Their unreachable bodies
can then hold hooks without removing combat XP or assuming unused RAM.
"""
from . import mips as m
from ..symbols import require
from .asm import Patch, packed
from .mips import jr


def prepare_gain_storage(pine, symbols):
    # Each stub's prologue spills its own arguments below SP (64-bit GPRs
    # via sd, the VEC3-taking stub's floats via swc1) then falls straight
    # into an unconditional return -- dead code the game never re-enters,
    # confirmed by this exact signature before any hook claims the space.
    text = [
        m.addiu(m.SP, m.SP, -112), m.sd(m.A3, 72, m.SP), m.sd(m.T0, 80, m.SP), m.sd(m.T1, 88, m.SP),
        m.sd(m.T2, 96, m.SP), m.sd(m.T3, 104, m.SP), m.swc1(m.F12, 56, m.SP), m.swc1(m.F14, 60, m.SP),
        m.swc1(m.F16, 64, m.SP), m.swc1(m.F18, 68, m.SP), jr(m.RA), m.addiu(m.SP, m.SP, 112),
    ]
    vector = [
        m.addiu(m.SP, m.SP, -112), m.sd(m.A2, 64, m.SP), m.sd(m.A3, 72, m.SP), m.sd(m.T0, 80, m.SP),
        m.sd(m.T1, 88, m.SP), m.sd(m.T2, 96, m.SP), m.sd(m.T3, 104, m.SP), m.swc1(m.F12, 48, m.SP),
        m.swc1(m.F14, 52, m.SP), m.swc1(m.F16, 56, m.SP), m.swc1(m.F18, 60, m.SP), jr(m.RA),
        m.addiu(m.SP, m.SP, 112),
    ]
    styled = [
        m.addiu(m.SP, m.SP, -96), m.sd(m.T0, 64, m.SP), m.sd(m.T1, 72, m.SP), m.sd(m.T2, 80, m.SP),
        m.sd(m.T3, 88, m.SP), m.swc1(m.F12, 48, m.SP), m.swc1(m.F14, 52, m.SP), m.swc1(m.F16, 56, m.SP),
        m.swc1(m.F18, 60, m.SP), jr(m.RA), m.addiu(m.SP, m.SP, 96),
    ]
    edits, ranges = [], []
    for name, words in (
            ('DEBUGDRAW_PrintText__FiiUie', text),
            ('DEBUGDRAW_PrintText__FPC4VEC3Uie', vector),
            ('DEBUGDRAW_PrintDropText__FiiUiUie', styled),
            ('DEBUGDRAW_PrintOutlineText__FiiUiUie', styled)):
        address = require(symbols, name)
        expected = packed(words)
        if pine.read_bytes(address, len(expected)) != expected:
            raise RuntimeError(f'Gain storage stub layout changed: {name}')
        edits.append(Patch(address, expected[:8], packed([jr(m.RA), m.NOP])))
        ranges.append((address + 8, address + len(expected)))
    if any(max(a, c) < min(b, d) for i, (a, b) in enumerate(ranges)
           for c, d in ranges[i + 1:]):
        raise RuntimeError('Gain storage stubs overlap')
    return edits, ranges

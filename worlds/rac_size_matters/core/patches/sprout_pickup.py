"""Intercept Ryllus' scripted Sprout-o-Matic handoff.

Retains removal of the pickup objects and the native sound. Replaces the
ownership grant and forced equip with a local check byte. Loader integration
and journal consumption are required before enabling this in Core.
"""
from . import mips as m
from .asm import Patch, branch, packed
from .plan import Plan


START = 0x00F06610
JOURNAL = START + 0x50
SIGNATURE = packed(
    0x27BDFFF0, 0x0080402D, 0xFFBF0000, 0x240A0002,
    0x24040011, 0x2406FFFF, 0x8D020064, 0x24070001,
    0x8D090058, 0x24050001, 0x34420020, 0xAD020064,
    0x8D230000, 0x8C620064, 0x34420020, 0xAC620064,
    0x0C356180, 0xA10A0045, 0x3C0400F8, 0x24050011,
    0x0C355C1C, 0x2484F1D0, 0x3C0200F6, 0x0C39B074,
    0x8C4422F0, 0xDFBF0000, 0x03E00008, 0x27BD0010,
)


def prepare(pine, *, checked=False, gate=None):
    held = gate.held_module() if gate is not None else None
    correct_level = (held is not None and held[0] == 2 and gate.pine is pine
                     if gate is not None else pine.read_int32(0x1F4C76C) == 2)
    if pine.get_game_id() != "SCUS-97615" or not correct_level:
        raise RuntimeError("Sprout pickup patch requires US PS2 Ryllus")
    if pine.read_bytes(START, len(SIGNATURE)) != SIGNATURE:
        raise RuntimeError("Sprout pickup signature changed")
    replacement = packed(
        m.lui(m.V0, (JOURNAL + 0x8000) >> 16),
        0xA10A0045,                         # retain object state change (original instruction)
        branch(START + 0x48, START + 0x58),
        m.sb(m.T2, JOURNAL & 0xFFFF, m.V0),   # t2 is still 2 (no setter call)
    ) + bytes([2 if checked else 1]) + b"SMPICK!"
    gate_address = START - 0xC4
    gate_original = packed(0x24040011, 0x0C3560EA, 0x2405FFFF)
    if pine.read_bytes(gate_address, 12) != gate_original:
        raise RuntimeError("Sprout pickup ownership gate changed")
    gate_code = packed(m.lui(m.V0, (JOURNAL + 0x8000) >> 16),
                       m.lbu(m.V0, JOURNAL & 0xFFFF, m.V0), m.addiu(m.V0, m.V0, -1))
    plan = Plan(pine, [Patch(START + 0x40, SIGNATURE[0x40:0x58], replacement),
                       Patch(gate_address, gate_original, gate_code)])
    plan.journals = ((JOURNAL, 1),)
    return plan

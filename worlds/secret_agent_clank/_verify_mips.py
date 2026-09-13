import sys
sys.path.insert(0, ".")
from worlds.secret_agent_clank.core.patches.asm import jump, packed
from worlds.secret_agent_clank.core.patches import mips as m


def old_flag_routine(table, fallback, *, record):
    code = [0x2C820028, 0, 0, 0x3C080000 | (table >> 16),
            0x35080000 | (table & 0xFFFF), 0x01044021, 0x91020000, 0, 0]
    code += ([0x24020002, 0xA1020000, 0x03E00008, 0] if record
             else [0x2442FFFF, 0x03E00008, 0])
    target = len(code)
    code += [jump(fallback), 0]
    for i in (1, 7):
        code[i] = 0x10400000 | (target - i - 1)
    return packed(code)


def old_entitlement_routine(table, gadget_base, fallback):
    owned = gadget_base + 0x70
    return packed([
        0x3C080000 | (table >> 16), 0x35080000 | (table & 0xFFFF),
        0x3C090000 | (owned >> 16), 0x35290000 | (owned & 0xFFFF),
        0x250A0028,
        0x910B0000,
        0x11600002, 0x256BFFFF,
        0xAD2B0000,
        0x25080001,
        0x150AFFFA, 0x25290074,
        0x910B0000, 0x256B0001, 0xA10B0000,
        jump(fallback), 0,
    ])


def new_flag_routine(table, fallback, *, record):
    code = [m.sltiu(m.V0, m.A0, 40), 0, 0,
            *m.li32(m.T0, table),
            m.addu(m.T0, m.T0, m.A0),
            m.lbu(m.V0, 0, m.T0), 0, 0]
    code += ([m.addiu(m.V0, m.ZERO, 2), m.sb(m.V0, 0, m.T0), m.jr(m.RA), 0] if record
             else [m.addiu(m.V0, m.V0, -1), m.jr(m.RA), 0])
    target = len(code)
    code += [jump(fallback), 0]
    for i in (1, 7):
        code[i] = m.beq(m.V0, m.ZERO, target - i - 1)
    return packed(code)


def new_entitlement_routine(table, gadget_base, fallback):
    owned = gadget_base + 0x70
    return packed([
        *m.li32(m.T0, table),
        *m.li32(m.T1, owned),
        m.addiu(m.T2, m.T0, 0x28),
        m.lbu(m.T3, 0, m.T0),
        m.beq(m.T3, m.ZERO, 2), m.addiu(m.T3, m.T3, -1),
        m.sw(m.T3, 0, m.T1),
        m.addiu(m.T0, m.T0, 1),
        m.bne(m.T0, m.T2, -6), m.addiu(m.T1, m.T1, 0x74),
        m.lbu(m.T3, 0, m.T0), m.addiu(m.T3, m.T3, 1), m.sb(m.T3, 0, m.T0),
        jump(fallback), 0,
    ])


import random
random.seed(0)
mismatches = 0
for _ in range(500):
    table = random.randrange(0, 0x2000000, 4)
    fallback = random.randrange(0, 0x2000000, 4)
    gadget_base = random.randrange(0, 0x2000000, 4)
    for record in (False, True):
        a = old_flag_routine(table, fallback, record=record)
        b = new_flag_routine(table, fallback, record=record)
        if a != b:
            mismatches += 1
            print("MISMATCH flag_routine", table, fallback, record)
            print(a.hex())
            print(b.hex())
    a = old_entitlement_routine(table, gadget_base, fallback)
    b = new_entitlement_routine(table, gadget_base, fallback)
    if a != b:
        mismatches += 1
        print("MISMATCH entitlement_routine", table, gadget_base, fallback)
        print(a.hex())
        print(b.hex())

print("mismatches:", mismatches)

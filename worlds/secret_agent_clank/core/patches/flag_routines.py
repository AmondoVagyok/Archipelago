"""Native routine generators shared by patches/weapon_pickup.py and
patches/vendor_only.py -- the two managed-ownership tables (pickup/vendor)
and the pre-init entitlement snapshot all read/write through one of these
two routine shapes.

Written with mips.py's mnemonics rather than raw hex words -- verified
byte-for-byte identical to the previous hand-packed encoding across 500
random (table, fallback, gadget_base) samples before this switch."""
from . import mips as m
from .asm import jump, packed


def flag_routine(table, fallback, *, record):
    """a0=gadget id. 0=unmanaged, 1=unchecked, 2=checked.

    Unmanaged ids tail-call the original function with its arguments intact.
    Managed grants only latch a location; they never change gameplay ownership.
    """
    code = [
        m.sltiu(m.V0, m.A0, 40),           # v0 = (a0 < 40) ? 1 : 0
        0, 0,                              # [1]=beq placeholder, [2]=its delay slot
        *m.li32(m.T0, table),              # t0 = table
        m.addu(m.T0, m.T0, m.A0),          # t0 = table + gadget id
        m.lbu(m.V0, 0, m.T0),              # v0 = *t0 (current flag byte)
        0, 0,                              # [7]=beq placeholder, [8]=its delay slot
    ]
    code += ([m.addiu(m.V0, m.ZERO, 2), m.sb(m.V0, 0, m.T0), m.jr(m.RA), 0] if record
             else [m.addiu(m.V0, m.V0, -1), m.jr(m.RA), 0])
    target = len(code)
    code += [jump(fallback), 0]
    for i in (1, 7):
        code[i] = m.beq(m.V0, m.ZERO, target - i - 1)
    return packed(code)


def entitlement_routine(table, gadget_base, fallback):
    """Apply managed AP ownership immediately before native object init.

    Forty bytes encode unmanaged=0, unowned=1, owned=2. The following byte
    counts invocations for the loading-time experiment. Only caller-saved
    temporaries change; the tail jump preserves the caller's return address.
    """
    owned = gadget_base + 0x70
    return packed([
        *m.li32(m.T0, table),                          # t0 = table
        *m.li32(m.T1, owned),                          # t1 = owned
        m.addiu(m.T2, m.T0, 0x28),                      # t2 = table end
        m.lbu(m.T3, 0, m.T0),                           # loop: t3 = *t0
        m.beq(m.T3, m.ZERO, 2), m.addiu(m.T3, m.T3, -1),  # unmanaged skips store; delay subtracts 1
        m.sw(m.T3, 0, m.T1),                            # *t1 = t3
        m.addiu(m.T0, m.T0, 1),                         # next table slot
        m.bne(m.T0, m.T2, -6), m.addiu(m.T1, m.T1, 0x74),  # loop; delay advances GadgetData slot
        m.lbu(m.T3, 0, m.T0), m.addiu(m.T3, m.T3, 1), m.sb(m.T3, 0, m.T0),  # invocation counter
        jump(fallback), 0,
    ])

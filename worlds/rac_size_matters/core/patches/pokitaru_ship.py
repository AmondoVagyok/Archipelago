"""Remove RatchetShip::Init's Ryllus prerequisite on Pokitaru only.

Verified against retail LEVEL_01.REL and live SCUS-97615 memory. This must
be installed before object initialization to affect the current visit. It
does not recreate a ship whose Init has already returned -1, and level loads
replace the patched code. Runtime loader integration is therefore required
before removing the existing combined-infobot compatibility behavior.
"""
from . import mips as m
from .asm import Patch, packed
from .plan import Plan


SITE = 0x00EEAB84
SIGNATURE_START = 0x00EEAB78
SIGNATURE = packed(
    0x24020001, 0x54620007, 0x8E320058,
    0x0C35CA9C, 0x24040002, 0x54400003, 0x8E320058,
    0x1000004B, 0x2402FFFF,
)


def prepare(pine, *, gate=None) -> Plan:
    if gate is not None:
        held = gate.held_module()
        if gate.pine is not pine or held is None or held[0] != 1:
            raise RuntimeError("Pokitaru must be held before level startup")
        delta = held[1] - 0xD4B380
    else:
        delta = 0
    if pine.get_game_id() != "SCUS-97615" or (gate is None and pine.read_int32(0x1F4C76C) != 1):
        raise RuntimeError("Ship patch requires US PS2 Pokitaru")
    # The call relocates with the module; the branch and register-relative
    # instructions do not. Derive its expected target from the loaded base.
    signature = bytearray(SIGNATURE)
    signature[12:16] = packed(0x0C000000 | ((0xD72A70 + delta) >> 2))
    if pine.read_bytes(SIGNATURE_START + delta, len(signature)) != signature:
        raise RuntimeError("Pokitaru ship initialization signature changed")
    # Replace only the call testing planet 2's availability. The existing
    # success branch loads s2 and continues normal ship initialization.
    return Plan(pine, [Patch(SITE + delta, bytes(signature[12:16]), packed(m.addiu(m.V0, m.ZERO, 1)))])

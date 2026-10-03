"""Pre-object-init ownership without rewriting pickup or vendor routines."""
from ...constants.native_functions import NativeFunctions
from ..symbols import require
from . import mips as m
from .asm import MARKER, Patch, jump, packed
from .entitlements import Entitlements
from .plan import PatchPlan
from .vendor_presentation import triangle_storage


class EquipmentOnly:
    def __init__(self, pine):
        self.pine = pine

    def prepare(self, symbols, checked, entitlements):
        p = self.pine
        storage, original = triangle_storage(p, symbols)
        marker = storage + 8
        data = bytearray(packed([m.jr(m.RA), m.NOP]) + MARKER)
        edits = []
        table = None
        if entitlements is not None:
            base, init, load, restart = require(
                symbols, "GADGET_g_GadgetList", NativeFunctions.MOBY_INIT_MOBYS,
                NativeFunctions.LEVEL_LOAD_LEVEL, NativeFunctions.LEVEL_RESTART)
            table = storage + len(data)
            flags = bytearray(44)
            for slot, value in entitlements.items():
                if not 0 <= slot < 40 or type(value) is not bool:
                    raise ValueError("Invalid AP entitlement")
                flags[slot] = 2 if value else 1
            data.extend(flags)
            routine = storage + len(data)
            data.extend(Entitlements(p).prepare(
                address=routine, table=table, gadget_base=base, fallback=init).replacement)
            for site in (load + 0x2F0, restart + 0x12C):
                if p.read_bytes(site, 8) != packed([jump(init, True), 0]):
                    raise RuntimeError("Object init call changed")
                edits.append(Patch(site, packed([jump(init, True)]), packed([jump(routine, True)])))
        # ConnectionWarning uses the tail of the same verified no-op routine.
        if len(data) > 152:
            raise RuntimeError("Equipment initialization overlaps connection warning storage")
        edits.insert(0, Patch(storage, original[:len(data)], bytes(data)))
        return PatchPlan(patches=edits, locations={}, tables={}, reported=set(checked),
                         marker_address=marker, module=p.read_int32(0x206328),
                         entitlement_table=table,
                         extra_ranges=[(storage + len(data), storage + 152)])

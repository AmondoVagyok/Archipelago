"""Native patch plan for modules with a vendor but no WeaponPickup code
(e.g. Treehouse). Reuses the bypassed vendor auto-equip tail, rather than
assuming spare memory or making pickup hooks optional where pickup code
exists -- see patches/weapon_pickup.py for the common case."""
from ..symbols import forbid, require
from .asm import MARKER, Patch, branch, jump, packed, words
from .flag_routines import entitlement_routine, flag_routine
from .plan import PatchPlan


def build_vendor_only_plan(p, symbols, locations, checked, entitlements):
    forbid(symbols, "WeaponPickup_UpdateWait__FP4Moby", "WeaponPickup_UpdateWaitForPickup__FP4Moby")
    get, put, sell, buy = require(symbols,
        "GADGET_PlayerHasGadget__FUi",
        "GADGET_SetGadgetOwnershipStatus__FUi24eGADGET_OWNERSHIP_STATUSb",
        "GADGET_IsSellable__FUi",
        "SCRNVENDOR_ProcessPurchase__Fv",
    )
    assert p.read_int32(sell + 12) == jump(get, True)
    assert p.read_int32(buy + 0x1EC) == jump(put, True)
    assert words(p.read_bytes(buy + 0x1F4, 8)) == [0x8E430010, 0x24020026]
    call = p.read_int32(buy + 0x338)
    assert call >> 26 == 3
    builder = (call & 0x3FFFFFF) << 2
    assert p.read_int32(builder) == 0x27BDFF70
    body = words(p.read_bytes(builder, 0x800))
    sites = [builder + i * 4 for i, w in enumerate(body) if w == jump(get, True)
             and next((body[j] for j in range(i - 1, max(-1, i - 7), -1)
                       if body[j] >> 26 == 3), None) == jump(sell, True)]
    assert len(sites) == 4
    reported = set(checked)
    plan_locations = {"vendor": dict(locations)} if locations else {}
    arena = buy + 0x1FC
    tables = {"vendor": arena + 16} if locations else {}
    flags = bytearray(40)
    for slot, name in locations.items():
        if not 0 <= slot < 40:
            raise ValueError("Invalid gadget id")
        flags[slot] = 2 if name in reported else 1
    data = bytearray(MARKER)
    if locations:
        data.extend(flags)
        getter = arena + len(data)
        data.extend(flag_routine(arena + 16, get, record=False))
        setter = arena + len(data)
        data.extend(flag_routine(arena + 16, put, record=True))
    init_edits = []
    entitlement_table = None
    if entitlements is not None:
        base, init, load, restart = require(symbols,
            "GADGET_g_GadgetList", "MOBY_InitMobys__Fv", "LEVEL_LoadLevel__FPCc", "LEVEL_Restart__Fv",
        )
        entitlement_table = arena + len(data)
        snapshot = bytearray(44)
        for slot, value in entitlements.items():
            if not 0 <= slot < 40 or type(value) is not bool:
                raise ValueError("Invalid AP entitlement")
            snapshot[slot] = 2 if value else 1
        data.extend(snapshot)
        routine = arena + len(data)
        data.extend(entitlement_routine(entitlement_table, base, init))
        for site in (load + 0x2F0, restart + 0x12C):
            assert words(p.read_bytes(site, 8)) == [jump(init, True), 0]
            init_edits.append((site, packed([jump(routine, True)])))
    assert arena + len(data) <= buy + 0x338
    edits = [(buy + 0x1F4, packed([branch(buy + 0x1F4, buy + 0x338), 0])),
             (arena, bytes(data))]
    if locations:
        edits.extend(((buy + 0x1EC, packed([jump(setter, True)])),
                      (sell + 12, packed([jump(getter, True)]))))
        edits.extend((site, packed([jump(getter, True)])) for site in sites)
    edits.extend(init_edits)
    patches = [Patch(a, p.read_bytes(a, len(b)), b) for a, b in edits]
    return PatchPlan(
        patches=patches, locations=plan_locations, tables=tables, reported=reported,
        marker_address=arena, module=p.read_int32(0x206328), entitlement_table=entitlement_table,
    )

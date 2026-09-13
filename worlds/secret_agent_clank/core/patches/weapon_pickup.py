"""Native patch plan for modules with WeaponPickup code -- the common case
(most levels have gadget pickups), combining pickup-grant, ownership-gate,
and vendor-purchase interception into one shared 40-byte-per-table scheme.

The intercepted pickup's native grant/presentation tail supplies storage for
the replacement routines and two independent 40-byte location tables. No free
RAM or allocator capacity is assumed. The original prologue and epilogue remain.
These patches require an explicit idle vendor test before runtime enablement.

See patches/vendor_only.py for modules (e.g. Treehouse) that only have
vendor code, reusing the vendor's own bypassed auto-equip tail instead."""
from ..symbols import require
from .asm import MARKER, Patch, branch, jump, packed, words
from .flag_routines import entitlement_routine, flag_routine
from .plan import PatchPlan


def build_weapon_pickup_plan(p, symbols, give, *, pickup_locations, vendor_locations, checked, entitlements):
    """Build a complete, signature-checked patch plan without writing RAM.

    `give` is WeaponPickup_GiveWeapon__FP4Moby's resolved address -- the
    caller (patches/hooks.py's LocationHooks.prepare()) already confirmed
    it exists before dispatching here; a missing export means this module
    has no pickup code at all, and build_vendor_only_plan() applies instead.
    """
    wait, wait_pickup, getter, setter, sellable, purchase = require(symbols,
        "WeaponPickup_UpdateWait__FP4Moby",
        "WeaponPickup_UpdateWaitForPickup__FP4Moby",
        "GADGET_PlayerHasGadget__FUi",
        "GADGET_SetGadgetOwnershipStatus__FUi24eGADGET_OWNERSHIP_STATUSb",
        "GADGET_IsSellable__FUi",
        "SCRNVENDOR_ProcessPurchase__Fv",
    )
    assert p.read_int32(give) == 0x27BDFF90, "Pickup prologue changed"
    assert p.read_int32(give + 0x50) == jump(setter, True), "Pickup grant call changed"
    assert p.read_int32(give + 0x54) == 0x2CC60002, "Pickup grant arguments changed"
    assert p.read_int32(give + 0x58) == 0x8E450000, "Pickup tail changed"
    assert words(p.read_bytes(give + 0x278, 28)) == [
        0xDFB00040, 0xDFB10048, 0xDFB20050, 0xDFB30058,
        0xDFBF0060, 0x03E00008, 0x27BD0070], "Pickup epilogue changed"
    assert p.read_int32(wait + 0x50) == jump(getter, True), "Pickup ownership gate changed"
    assert p.read_int32(wait + 0x54) == 0x8E640000, "Pickup gate arguments changed"
    assert p.read_int32(wait_pickup + 0x48) == jump(getter, True), "Collection ownership gate changed"
    assert p.read_int32(wait_pickup + 0x4C) == 0x8E040000, "Collection gate arguments changed"
    assert p.read_int32(sellable + 12) == jump(getter, True), "Sellable gate changed"
    assert p.read_int32(purchase + 0x1EC) == jump(setter, True), "Purchase grant changed"
    assert words(p.read_bytes(purchase + 0x1F4, 8)) == [0x8E430010, 0x24020026]
    builder_call = p.read_int32(purchase + 0x338)
    assert builder_call >> 26 == 3, "Vendor rebuild call changed"
    builder = (builder_call & 0x03FFFFFF) << 2
    assert p.read_int32(builder) == 0x27BDFF70, "Vendor builder changed"
    body = words(p.read_bytes(builder, 0x800))
    # Only base-offer ownership calls immediately following IsSellable.
    # Ammo and mod ownership calls retain their gameplay semantics.
    sites = []
    for i, instruction in enumerate(body):
        if instruction != jump(getter, True):
            continue
        previous_call = next((body[j] for j in range(i - 1, max(-1, i - 7), -1)
                              if body[j] >> 26 == 3), None)
        if previous_call == jump(sellable, True):
            sites.append(builder + i * 4)
    assert len(sites) == 4, f"Unexpected base-offer gates: {len(sites)}"

    locations = {"pickup": dict(pickup_locations), "vendor": dict(vendor_locations)}
    for mapping in locations.values():
        if any(not 0 <= slot < 40 for slot in mapping):
            raise ValueError("Gadget ids must be between 0 and 39")
    reported = set(checked)
    arena = give + 0x60
    pickup_table, vendor_table = arena + 16, arena + 56
    tables = {"pickup": pickup_table, "vendor": vendor_table}
    data = bytearray(MARKER)
    assert len(data) == 16
    for kind in ("pickup", "vendor"):
        flags = bytearray(40)
        for slot, name in locations[kind].items():
            flags[slot] = 2 if name in reported else 1
        data.extend(flags)
    routines = {}
    for kind, record in (("pickup", False), ("pickup", True), ("vendor", False), ("vendor", True)):
        routines[kind, record] = arena + len(data)
        data.extend(flag_routine(tables[kind], setter if record else getter, record=record))
    init_edits = []
    entitlement_table = None
    if entitlements is not None:
        if any(not 0 <= slot < 40 or type(value) is not bool for slot, value in entitlements.items()):
            raise ValueError("Entitlements require gadget ids 0..39 and boolean ownership")
        base, init, load, restart = require(symbols,
            "GADGET_g_GadgetList", "MOBY_InitMobys__Fv", "LEVEL_LoadLevel__FPCc", "LEVEL_Restart__Fv",
        )
        for site in (load + 0x2F0, restart + 0x12C):
            assert words(p.read_bytes(site, 8)) == [jump(init, True), 0], "Object init call changed"
        entitlement_table = arena + len(data)
        flags = bytearray(44)  # 40 slots, invocation byte, alignment padding
        for slot, value in entitlements.items():
            flags[slot] = 2 if value else 1
        data.extend(flags)
        routine = arena + len(data)
        data.extend(entitlement_routine(entitlement_table, base, init))
        init_edits = [(site, packed([jump(routine, True)]))
                      for site in (load + 0x2F0, restart + 0x12C)]
    assert arena + len(data) <= give + 0x278, "Replacement exceeds intercepted tail"
    edits = [(give + 0x58, packed([branch(give + 0x58, give + 0x278), 0])),
             (arena, bytes(data)),
             (give + 0x50, packed([jump(routines["pickup", True], True)])),
             (wait + 0x50, packed([jump(routines["pickup", False], True)])),
             (wait_pickup + 0x48, packed([jump(routines["pickup", False], True)])),
             (sellable + 12, packed([jump(routines["vendor", False], True)])),
             (purchase + 0x1EC, packed([jump(routines["vendor", True], True)])),
             (purchase + 0x1F4, packed([branch(purchase + 0x1F4, purchase + 0x338), 0]))]
    edits.extend((site, packed([jump(routines["vendor", False], True)])) for site in sites)
    edits.extend(init_edits)
    patches = [Patch(a, p.read_bytes(a, len(b)), b) for a, b in edits]
    return PatchPlan(
        patches=patches, locations=locations, tables=tables, reported=reported,
        marker_address=arena, module=p.read_int32(0x206328), entitlement_table=entitlement_table,
    )

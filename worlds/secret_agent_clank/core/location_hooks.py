"""Experimental native location interception for SCUS-97623.

The intercepted pickup's native grant/presentation tail supplies storage for
the replacement routines and two independent 40-byte location tables. No free
RAM or allocator capacity is assumed. The original prologue and epilogue remain.
These patches require an explicit idle vendor test before runtime enablement.
"""
import struct
from dataclasses import dataclass

if not __debug__:
    raise RuntimeError('Native hook validation must not run with Python assertions disabled')

MARKER = b'SAC_LOC_HOOK_V1\0'

# Existing AP location names, separated by the native source of collection.
VENDOR_LOCATIONS = {
    5: 'shockrocket', 7: 'plasmawhip', 8: 'porkbomb', 10: 'ryno',
    14: 'HoloKnuckles', 16: 'LightningUmbrella', 18: 'hypnowatch',
    26: 'clankpda', 35: 'boltgrabber', 37: 'superkick',
    38: 'kickblast', 39: 'kicksplosion',
}
PICKUP_LOCATIONS = {
    2: 'blaster', 3: 'shardgun', 4: 'beemineglove', 6: 'walloper',
    9: 'minelauncher', 11: 'throwTie', 12: 'CuffLink', 13: 'TangleVine',
    15: 'FlamethrowerPen', 17: 'Black Out Pen (Pickup)',
    # No 23 (ratchetpda): granted as the reward for The Showers' "No good
    # deed goes unpunished." Ratchet Challenge, not a separate native pickup
    # event -- that challenge's own location already covers this moment
    # (see constants/weapons.py's WEAPONS_BY_CASE, which no longer places
    # RATCHETPDA in any case).
    # No 27 (bolttransfer): granted as the reward for one of Prison
    # Breakout!'s Ratchet Challenges, not a separate native pickup event --
    # that challenge's own location already covers this moment (see
    # constants/weapons.py's WEAPONS_BY_CASE, which no longer places
    # BOLTTRANSFER in any case).
    24: 'holomonocle', 32: 'jetboots', 33: 'omnikey',
}


def words(data):
    return list(struct.unpack('<' + 'I' * (len(data) // 4), data))


def packed(values):
    return struct.pack('<' + 'I' * len(values), *values)


def jump(address, link=False):
    if address % 4:
        raise ValueError('MIPS jump target must be word aligned')
    return (0x0C000000 if link else 0x08000000) | (address >> 2)


def branch(source, target):
    return 0x10000000 | (((target - source - 4) // 4) & 0xFFFF)


def flag_routine(table, fallback, *, record):
    """a0=gadget id. 0=unmanaged, 1=unchecked, 2=checked.

    Unmanaged ids tail-call the original function with its arguments intact.
    Managed grants only latch a location; they never change gameplay ownership.
    """
    code = [0x2C820028, 0, 0, 0x3C080000 | (table >> 16),
            0x35080000 | (table & 0xFFFF), 0x01044021, 0x91020000, 0, 0]
    code += ([0x24020002, 0xA1020000, 0x03E00008, 0] if record
             else [0x2442FFFF, 0x03E00008, 0])
    target = len(code)
    code += [jump(fallback), 0]
    for i in (1, 7):
        code[i] = 0x10400000 | (target - i - 1)
    return packed(code)


def entitlement_routine(table, gadget_base, fallback):
    """Apply managed AP ownership immediately before native object init.

    Forty bytes encode unmanaged=0, unowned=1, owned=2. The following byte
    counts invocations for the loading-time experiment. Only caller-saved
    temporaries change; the tail jump preserves the caller's return address.
    """
    owned = gadget_base + 0x70
    return packed([
        0x3C080000 | (table >> 16), 0x35080000 | (table & 0xFFFF),
        0x3C090000 | (owned >> 16), 0x35290000 | (owned & 0xFFFF),
        0x250A0028,                 # t2 = table end
        0x910B0000,                 # loop: lbu t3, 0(t0)
        0x11600002, 0x256BFFFF,     # unmanaged skips store; delay subtracts 1
        0xAD2B0000,                 # sw t3, 0(t1)
        0x25080001,                 # next table slot
        0x150AFFFA, 0x25290074,     # loop; delay advances GadgetData slot
        0x910B0000, 0x256B0001, 0xA10B0000,  # invocation counter
        jump(fallback), 0,
    ])


@dataclass(frozen=True)
class Patch:
    address: int
    original: bytes
    replacement: bytes


class LocationHooks:
    def __init__(self, pine):
        self.pine = pine
        self.patches = []
        self.module = None
        self.marker_address = None
        self.tables = {}
        self.locations = {}
        self.reported = set()
        self.installed = False
        self.entitlement_table = None

    def prepare(self, symbols, *, pickup_locations, vendor_locations, checked=(), entitlements=None):
        """Build a complete, signature-checked patch plan without writing RAM."""
        self.extra_ranges = []
        if self.installed:
            raise RuntimeError('Restore installed hooks before preparing a new plan')
        p = self.pine
        give = symbols.get('WeaponPickup_GiveWeapon__FP4Moby')
        if give is None:
            return self._prepare_vendor_only(symbols, vendor_locations, checked, entitlements)
        wait = symbols.get('WeaponPickup_UpdateWait__FP4Moby')
        wait_pickup = symbols.get('WeaponPickup_UpdateWaitForPickup__FP4Moby')
        getter = symbols.get('GADGET_PlayerHasGadget__FUi')
        setter = symbols.get('GADGET_SetGadgetOwnershipStatus__FUi24eGADGET_OWNERSHIP_STATUSb')
        sellable = symbols.get('GADGET_IsSellable__FUi')
        purchase = symbols.get('SCRNVENDOR_ProcessPurchase__Fv')
        if None in (give, wait, wait_pickup, getter, setter, sellable, purchase):
            raise ValueError('Required native exports missing')
        assert p.read_int32(give) == 0x27BDFF90, 'Pickup prologue changed'
        assert p.read_int32(give + 0x50) == jump(setter, True), 'Pickup grant call changed'
        assert p.read_int32(give + 0x54) == 0x2CC60002, 'Pickup grant arguments changed'
        assert p.read_int32(give + 0x58) == 0x8E450000, 'Pickup tail changed'
        assert words(p.read_bytes(give + 0x278, 28)) == [
            0xDFB00040, 0xDFB10048, 0xDFB20050, 0xDFB30058,
            0xDFBF0060, 0x03E00008, 0x27BD0070], 'Pickup epilogue changed'
        assert p.read_int32(wait + 0x50) == jump(getter, True), 'Pickup ownership gate changed'
        assert p.read_int32(wait + 0x54) == 0x8E640000, 'Pickup gate arguments changed'
        assert p.read_int32(wait_pickup + 0x48) == jump(getter, True), 'Collection ownership gate changed'
        assert p.read_int32(wait_pickup + 0x4C) == 0x8E040000, 'Collection gate arguments changed'
        assert p.read_int32(sellable + 12) == jump(getter, True), 'Sellable gate changed'
        assert p.read_int32(purchase + 0x1EC) == jump(setter, True), 'Purchase grant changed'
        assert words(p.read_bytes(purchase + 0x1F4, 8)) == [0x8E430010, 0x24020026]
        builder_call = p.read_int32(purchase + 0x338)
        assert builder_call >> 26 == 3, 'Vendor rebuild call changed'
        builder = (builder_call & 0x03FFFFFF) << 2
        assert p.read_int32(builder) == 0x27BDFF70, 'Vendor builder changed'
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
        assert len(sites) == 4, f'Unexpected base-offer gates: {len(sites)}'

        self.locations = {'pickup': dict(pickup_locations), 'vendor': dict(vendor_locations)}
        for mapping in self.locations.values():
            if any(not 0 <= slot < 40 for slot in mapping):
                raise ValueError('Gadget ids must be between 0 and 39')
        self.reported = set(checked)
        arena = give + 0x60
        pickup_table, vendor_table = arena + 16, arena + 56
        self.tables = {'pickup': pickup_table, 'vendor': vendor_table}
        data = bytearray(MARKER)
        assert len(data) == 16
        for kind in ('pickup', 'vendor'):
            flags = bytearray(40)
            for slot, name in self.locations[kind].items():
                flags[slot] = 2 if name in self.reported else 1
            data.extend(flags)
        routines = {}
        for kind, record in (('pickup', False), ('pickup', True), ('vendor', False), ('vendor', True)):
            routines[kind, record] = arena + len(data)
            data.extend(flag_routine(self.tables[kind], setter if record else getter, record=record))
        init_edits = []
        self.entitlement_table = None
        if entitlements is not None:
            if any(not 0 <= slot < 40 or type(value) is not bool for slot, value in entitlements.items()):
                raise ValueError('Entitlements require gadget ids 0..39 and boolean ownership')
            base = symbols.get('GADGET_g_GadgetList')
            init = symbols.get('MOBY_InitMobys__Fv')
            load = symbols.get('LEVEL_LoadLevel__FPCc')
            restart = symbols.get('LEVEL_Restart__Fv')
            if None in (base, init, load, restart):
                raise ValueError('Pre-initialization exports missing')
            for site in (load + 0x2F0, restart + 0x12C):
                assert words(p.read_bytes(site, 8)) == [jump(init, True), 0], 'Object init call changed'
            self.entitlement_table = arena + len(data)
            flags = bytearray(44)  # 40 slots, invocation byte, alignment padding
            for slot, value in entitlements.items():
                flags[slot] = 2 if value else 1
            data.extend(flags)
            routine = arena + len(data)
            data.extend(entitlement_routine(self.entitlement_table, base, init))
            init_edits = [(site, packed([jump(routine, True)]))
                          for site in (load + 0x2F0, restart + 0x12C)]
        assert arena + len(data) <= give + 0x278, 'Replacement exceeds intercepted tail'
        edits = [(give + 0x58, packed([branch(give + 0x58, give + 0x278), 0])),
                 (arena, bytes(data)),
                 (give + 0x50, packed([jump(routines['pickup', True], True)])),
                 (wait + 0x50, packed([jump(routines['pickup', False], True)])),
                 (wait_pickup + 0x48, packed([jump(routines['pickup', False], True)])),
                 (sellable + 12, packed([jump(routines['vendor', False], True)])),
                 (purchase + 0x1EC, packed([jump(routines['vendor', True], True)])),
                 (purchase + 0x1F4, packed([branch(purchase + 0x1F4, purchase + 0x338), 0]))]
        edits.extend((site, packed([jump(routines['vendor', False], True)])) for site in sites)
        edits.extend(init_edits)
        self.patches = [Patch(a, p.read_bytes(a, len(b)), b) for a, b in edits]
        self.marker_address = arena
        self.module = p.read_int32(0x206328)
        return len(self.patches)

    def _prepare_vendor_only(self, symbols, locations, checked, entitlements):
        """Modules such as Treehouse have a vendor but no WeaponPickup code.

        Reuse the bypassed vendor auto-equip tail, rather than assuming spare
        memory or making pickup hooks optional where pickup code exists.
        """
        p = self.pine
        if any(symbols.get(n) is not None for n in ('WeaponPickup_UpdateWait__FP4Moby',
                                                   'WeaponPickup_UpdateWaitForPickup__FP4Moby')):
            raise ValueError('Incomplete pickup exports')
        get = symbols.get('GADGET_PlayerHasGadget__FUi')
        put = symbols.get('GADGET_SetGadgetOwnershipStatus__FUi24eGADGET_OWNERSHIP_STATUSb')
        sell = symbols.get('GADGET_IsSellable__FUi')
        buy = symbols.get('SCRNVENDOR_ProcessPurchase__Fv')
        if None in (get, put, sell, buy):
            raise ValueError('Required vendor exports missing')
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
        self.reported = set(checked)
        self.locations = {'vendor': dict(locations)} if locations else {}
        arena = buy + 0x1FC
        self.tables = {'vendor': arena + 16} if locations else {}
        flags = bytearray(40)
        for slot, name in locations.items():
            if not 0 <= slot < 40:
                raise ValueError('Invalid gadget id')
            flags[slot] = 2 if name in self.reported else 1
        data = bytearray(MARKER)
        if locations:
            data.extend(flags)
            getter = arena + len(data)
            data.extend(flag_routine(arena + 16, get, record=False))
            setter = arena + len(data)
            data.extend(flag_routine(arena + 16, put, record=True))
        init_edits = []
        self.entitlement_table = None
        if entitlements is not None:
            base, init, load, restart = [symbols.get(n) for n in ('GADGET_g_GadgetList',
                'MOBY_InitMobys__Fv', 'LEVEL_LoadLevel__FPCc', 'LEVEL_Restart__Fv')]
            if None in (base, init, load, restart):
                raise ValueError('Pre-initialization exports missing')
            self.entitlement_table = arena + len(data)
            snapshot = bytearray(44)
            for slot, value in entitlements.items():
                if not 0 <= slot < 40 or type(value) is not bool:
                    raise ValueError('Invalid AP entitlement')
                snapshot[slot] = 2 if value else 1
            data.extend(snapshot)
            routine = arena + len(data)
            data.extend(entitlement_routine(self.entitlement_table, base, init))
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
        self.patches = [Patch(a, p.read_bytes(a, len(b)), b) for a, b in edits]
        self.marker_address = arena
        self.module = p.read_int32(0x206328)
        return len(self.patches)

    def install(self, screen_address):
        """Research-only: install in an idle vendor/Case Files, without input."""
        p = self.pine
        if not self.patches or self.installed:
            raise RuntimeError('No fresh patch plan')
        assert p.get_game_id() == 'SCUS-97623'
        assert p.read_int32(0x206328) == self.module and p.read_int32(0x206324) == 0xFFFFFFFF
        assert p.read_int32(screen_address) in (8, 14, 16), 'Open vendor or Case Files before installing'
        self._install_plan()

    def install_at_loader_gate(self, gate):
        """Experimental installation before the native level thread starts."""
        if gate.pine is not self.pine:
            raise RuntimeError('Loader barrier must share this PINE connection')
        target = gate.held_module()
        if target is None:
            raise RuntimeError('New level is not held before startup')
        if not self.patches or self.installed:
            raise RuntimeError('No fresh patch plan')
        self.module = target
        self._install_plan()

    def _install_plan(self):
        p = self.pine
        for patch in self.patches:
            assert p.read_bytes(patch.address, len(patch.original)) == patch.original, 'Code changed since planning'
        attempted = []
        try:
            for patch in self.patches:
                attempted.append(patch)
                p.write_bytes(patch.address, patch.replacement)
            for patch in self.patches:
                assert p.read_bytes(patch.address, len(patch.replacement)) == patch.replacement
            for kind, table in self.tables.items():
                flags = p.read_bytes(table, 40)
                for slot, name in self.locations[kind].items():
                    unchecked = 3 if kind == 'titan' else 1
                    assert flags[slot] == (2 if name in self.reported else unchecked)
        except Exception:
            # Caller keeps native execution parked throughout installation.
            # Undo even a partially transmitted write before releasing it.
            for patch in reversed(attempted):
                p.write_bytes(patch.address, patch.original)
                if p.read_bytes(patch.address, len(patch.original)) != patch.original:
                    raise RuntimeError('Hook installation rollback readback failed')
            raise
        self.installed = True

    def poll(self):
        if not self.installed:
            return []
        if not self.is_current():
            # A savestate or same-level reload can replace code without
            # changing the module id. The client must install again.
            self.installed = False
            return []
        found = []
        for kind, table in self.tables.items():
            flags = self.pine.read_bytes(table, 40)
            for slot, name in self.locations[kind].items():
                if flags[slot] == 2 and name not in self.reported:
                    found.append(name)
                    self.reported.add(name)
        return found

    def is_current(self):
        return (self.marker_address is not None
                and self.pine.read_int32(0x206328) == self.module
                and self.pine.read_bytes(self.marker_address, len(MARKER)) == MARKER)

    def sync_checked(self, checked):
        """Server-confirmed checks suppress offers/spawns, never grant items."""
        if not self.installed:
            self.reported.update(checked)
            return
        if not self.is_current():
            self.installed = False
            return
        checked = set(checked)
        writes = [(self.tables[kind] + slot, 2)
                  for kind, mapping in self.locations.items()
                  for slot, name in mapping.items() if name in checked
                  and self.pine.read_int8(self.tables[kind] + slot) != 2]
        if writes:
            self.pine.batch_write_int8(writes)
        self.reported.update(checked)

    def sync_entitlements(self, entitlements):
        """Keep the pre-object-init snapshot current for native restarts too."""
        if self.entitlement_table is None or not self.installed or not self.is_current():
            return
        flags = bytearray(40)
        for slot, value in entitlements.items():
            if not 0 <= slot < 40 or type(value) is not bool:
                raise ValueError('Invalid AP entitlement')
            flags[slot] = 2 if value else 1
        if self.pine.read_bytes(self.entitlement_table, 40) != flags:
            self.pine.write_bytes(self.entitlement_table, bytes(flags))

    def restore(self):
        if not self.installed:
            return
        p = self.pine
        assert p.get_game_id() == 'SCUS-97623'
        assert p.read_int32(0x206328) == self.module and p.read_int32(0x206324) == 0xFFFFFFFF
        assert p.read_bytes(self.marker_address, len(MARKER)) == MARKER
        # Restore entry calls before reclaiming their routines, and restore
        # the original pickup tail branch last.
        for patch in reversed(self.patches):
            p.write_bytes(patch.address, patch.original)
        self.installed = False

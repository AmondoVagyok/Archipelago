"""Native location interception: picks the patch plan for the loaded module and installs, polls and restores it."""
from ...constants import EQUIPMENT_INTERNAL_TO_DISPLAY, NativeFunctions, vendor_location_name
from ..batch_io import read_blocks, write_blocks
from .asm import MARKER, packed
from .vendor_only import VendorOnly
from .weapon_pickup import WeaponPickup
from .equipment_only import EquipmentOnly


class LocationHooks:
    def __init__(self, pine):
        # Checked here rather than at import so generation/fuzzing under -O can still load the world.
        if not __debug__:
            raise RuntimeError("Native hook validation must not run with Python assertions disabled")
        self.pine = pine
        self.patches = []
        self.module = None
        self.marker_address = None
        self.tables = {}
        self.locations = {}
        self.reported = set()
        self.installed = False
        self.entitlement_table = None
        self.extra_ranges = []
        self.gain_storage_prepared = False
        self.catalog_only_ranges = []

    def prepare(self, symbols, *, pickup_locations, vendor_locations, checked=(), entitlements=None,
                vendor_enabled=True):
        """Build a complete, signature-checked patch plan without writing RAM."""
        self.extra_ranges = []
        self.gain_storage_prepared = False
        self.catalog_only_ranges = []
        if self.installed:
            raise RuntimeError("Restore installed hooks before preparing a new plan")
        pickup_locations = {slot: EQUIPMENT_INTERNAL_TO_DISPLAY.get(name, name)
                            for slot, name in pickup_locations.items()}
        vendor_locations = {slot: vendor_location_name(EQUIPMENT_INTERNAL_TO_DISPLAY.get(name, name))
                            for slot, name in vendor_locations.items()}
        p = self.pine
        give = symbols.get(NativeFunctions.WEAPON_PICKUP_GIVE_WEAPON)
        if give is None and not vendor_enabled:
            plan = EquipmentOnly(p).prepare(symbols, checked, entitlements)
        elif give is None:
            plan = VendorOnly(p).prepare(symbols, vendor_locations, checked, entitlements)
        else:
            plan = WeaponPickup(p).prepare(
                symbols, give, pickup_locations=pickup_locations,
                vendor_locations=vendor_locations, checked=checked, entitlements=entitlements,
                vendor_enabled=vendor_enabled,
            )
        self.patches = plan.patches
        self.locations = plan.locations
        self.tables = plan.tables
        self.reported = plan.reported
        self.marker_address = plan.marker_address
        self.module = plan.module
        self.entitlement_table = plan.entitlement_table
        self.extra_ranges = plan.extra_ranges
        return len(self.patches)

    def install(self, screen_address):
        """Research-only: install in an idle vendor/Case Files, without input."""
        p = self.pine
        if not self.patches or self.installed:
            raise RuntimeError("No fresh patch plan")
        assert p.get_game_id() == "SCUS-97623"
        module, status, screen = p.batch_read_int32([0x206328, 0x206324, screen_address])
        assert module == self.module and status == 0xFFFFFFFF
        assert screen in (8, 14, 16), "Open vendor or Case Files before installing"
        self._install_plan()

    def install_at_loader_gate(self, gate):
        """Experimental installation before the native level thread starts."""
        if gate.pine is not self.pine:
            raise RuntimeError("Loader barrier must share this PINE connection")
        target = gate.held_module()
        if target is None:
            raise RuntimeError("New level is not held before startup")
        if not self.patches or self.installed:
            raise RuntimeError("No fresh patch plan")
        self.module = target
        self._install_plan()

    def _install_plan(self):
        p = self.pine
        originals = [patch.original for patch in self.patches]
        replacements = [patch.replacement for patch in self.patches]
        current = read_blocks(p, [(patch.address, len(patch.original)) for patch in self.patches])
        assert current == originals, "Code changed since planning"
        tables = list(self.tables.items())
        try:
            write_blocks(p, [(patch.address, patch.replacement) for patch in self.patches])
            readback = read_blocks(p, [*((patch.address, len(patch.replacement)) for patch in self.patches),
                                       *((table, 40) for _, table in tables)])
            assert readback[:len(self.patches)] == replacements
            for (kind, _), flags in zip(tables, readback[len(self.patches):]):
                for slot, name in self.locations[kind].items():
                    unchecked = 3 if kind == "titan" else 1
                    assert flags[slot] == (2 if name in self.reported else unchecked)
        except Exception as err:
            # Caller keeps native execution parked throughout installation.
            # Undo even a partially transmitted write before releasing it.
            write_blocks(p, [(patch.address, patch.original) for patch in reversed(self.patches)])
            if read_blocks(p, [(patch.address, len(patch.original)) for patch in self.patches]) != originals:
                raise RuntimeError("Hook installation rollback readback failed") from err
            raise
        self.installed = True

    def poll(self):
        if not self.installed:
            return []
        tables = self._read_if_current([(table, 40) for table in self.tables.values()])
        if tables is None:
            # A savestate or same-level reload can replace code without
            # changing the module id. The client must install again.
            self.installed = False
            return []
        found = []
        for kind, flags in zip(self.tables, tables):
            for slot, name in self.locations[kind].items():
                if flags[slot] == 2 and name not in self.reported:
                    found.append(name)
                    self.reported.add(name)
        return found

    def is_current(self):
        return self._read_if_current([]) is not None

    def _read_if_current(self, spans):
        if self.marker_address is None:
            return None
        module, marker, *data = read_blocks(self.pine, [(0x206328, 4), (self.marker_address, len(MARKER)), *spans])
        if int.from_bytes(module, "little") != self.module or marker != MARKER:
            return None
        return data

    def sync_checked(self, checked):
        """Server-confirmed checks suppress offers/spawns, never grant items."""
        if not self.installed:
            self.reported.update(checked)
            return
        kinds = list(self.locations)
        tables = self._read_if_current([(self.tables[kind], 40) for kind in kinds])
        if tables is None:
            self.installed = False
            return
        checked = set(checked)
        writes = [(self.tables[kind] + slot, 2)
                  for kind, flags in zip(kinds, tables)
                  for slot, name in self.locations[kind].items() if name in checked and flags[slot] != 2]
        if writes:
            self.pine.batch_write_int8(writes)
        self.reported.update(checked)

    def sync_entitlements(self, entitlements):
        """Keep the pre-object-init snapshot current for native restarts too."""
        if self.entitlement_table is None or not self.installed:
            return
        flags = bytearray(40)
        for slot, value in entitlements.items():
            if not 0 <= slot < 40 or type(value) is not bool:
                raise ValueError("Invalid AP entitlement")
            flags[slot] = 2 if value else 1
        current = self._read_if_current([(self.entitlement_table, 40)])
        if current is not None and current[0] != flags:
            self.pine.write_bytes(self.entitlement_table, bytes(flags))

    def restore(self):
        if not self.installed:
            return
        p = self.pine
        assert p.get_game_id() == "SCUS-97623"
        assert self._read_if_current([(0x206324, 4)]) == [packed([0xFFFFFFFF])]
        # Restore entry calls before reclaiming their routines, and restore
        # the original pickup tail branch last.
        write_blocks(p, [(patch.address, patch.original) for patch in reversed(self.patches)])
        self.installed = False

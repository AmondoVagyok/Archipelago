"""Install native location hooks before each loaded module starts gameplay."""
from ..constants.native_modules import CASE_MODULES
from ..constants.vendor import vendor_location_name
from ..constants.weapons import EQUIPMENT_INTERNAL_TO_DISPLAY
from .address_maps import CURRENT_CASE_ADDRESS, FORCE_CASE_ADDRESS
from .main_menu import is_main_menu
from .patches import PICKUP_LOCATIONS, VENDOR_LOCATIONS
from .patches.connection_warning import ConnectionWarning
from .patches.loader_gate import LoaderGate
from .patches.mission_travel import MissionTravel
from .patches.starting_case import StartingCase
from .patches.titan_vendor import TitanOffers, TitanVendor
from .patches.vendor_catalog import VendorCatalog
from .symbols import RuntimeSymbols


class NativeRuntime:
    def __init__(self, pine, hooks, log):
        self.pine, self.hooks, self.log = pine, hooks, log
        self.gate = LoaderGate(pine)
        self.awaiting_start = False
        self.reload_requested = False
        self.generation = 0
        self.wrench = None
        self.progression = None
        self.weapon_mods = None
        self.skins = None
        self.vendor_modules = None
        self.vendor_locations = None
        self.vendor_catalog = None
        self.presentation = None
        self.connection_warning = ConnectionWarning(pine)
        self.ap_connected = False
        self.owned_cases = frozenset()
        self.starting_case = StartingCase(pine, log)

    def configure_vendors(self, case_names):
        self.vendor_modules = {CASE_MODULES[name] for name in case_names}

    def service(self, checked, entitlements):
        """Return True only when gameplay may use this module's installed hooks."""
        p = self.pine
        try:
            if self.starting_case.service():
                self.awaiting_start = False
                self.hooks.installed = False
                if not self.gate.armed:
                    self.gate.arm()
                return False
            if self.awaiting_start:
                if (p.read_int32(self.gate.STATE) == 4
                        or p.read_int32(0x206324) != 0xFFFFFFFF
                        or p.read_int32(0x206338) != 3):
                    return False
                if (p.read_int32(0x206328) != self.hooks.module
                        or (self.hooks.entitlement_table is not None
                            and not p.read_int8(self.hooks.entitlement_table + 40))):
                    return False
                self.awaiting_start = False
            if not self.gate.armed:
                self.gate.arm()
            target = self.gate.held_module()
            if target == 0:
                self.hooks.installed = False
                self.awaiting_start = False
                self.reload_requested = False
                self.gate.release()
                return False
            if target is not None:
                stealth = getattr(self.progression, "stealth", None)
                if stealth is not None and stealth.mode and not stealth.loaded:
                    return False  # Keep the loader parked until slot progress is known.
                symbols = RuntimeSymbols(p)
                symbols.refresh()
                self.hooks.installed = False
                vendor_enabled = self.vendor_modules is None or target in self.vendor_modules
                self.hooks.prepare(symbols, pickup_locations=PICKUP_LOCATIONS,
                                   vendor_locations={slot: name for slot, name in VENDOR_LOCATIONS.items()
                                       if vendor_enabled and (self.vendor_locations is None or
                                           vendor_location_name(EQUIPMENT_INTERNAL_TO_DISPLAY.get(name, name)) in self.vendor_locations)}, checked=checked,
                                   entitlements=entitlements)
                if self.wrench is not None:
                    self.hooks.patches.extend(self.wrench.prepare(symbols, target))
                self.hooks.patches.extend(MissionTravel(p).prepare(symbols))
                if self.skins is not None:
                    self.hooks.patches.extend(self.skins.prepare(symbols))
                if self.weapon_mods is not None:
                    self.hooks.patches.extend(self.weapon_mods.prepare(
                        symbols, self.hooks, target, checked, vendor_enabled))
                if self.progression is not None:
                    if self.progression.max_challenge_mode and vendor_enabled:
                        self.hooks.patches.extend(TitanVendor(p).prepare(symbols, self.hooks, checked, self.vendor_locations))
                    elif vendor_enabled:
                        self.hooks.patches.extend(TitanOffers(p).prepare(symbols))
                self.vendor_catalog = VendorCatalog(p) if vendor_enabled else None
                if self.vendor_catalog is not None:
                    self.hooks.patches.extend(self.vendor_catalog.prepare(symbols, self.hooks))
                if self.presentation is not None and vendor_enabled:
                    self.hooks.patches.extend(self.presentation.prepare(symbols, self.hooks))
                self.hooks.patches.extend(self.connection_warning.prepare(symbols, self.hooks))
                if self.progression is not None:
                    self.hooks.patches.extend(self.progression.prepare(
                        symbols, self.hooks, target, vendor_enabled=vendor_enabled))
                self.hooks.install_at_loader_gate(self.gate)
                if self.vendor_catalog is not None:
                    self.vendor_catalog.challenge_level = self.progression.ng_plus if self.progression is not None else 0
                    self.vendor_catalog.sync_cases(self.owned_cases)
                if self.skins is not None:
                    self.skins.sync()
                self.connection_warning.refresh(self.ap_connected)
                self.generation += 1
                self.gate.release()
                self.awaiting_start = True
                self.reload_requested = False
                self.log(f"[SAC] Hooks loaded for {target}")
                return False
            if is_main_menu(p):
                self.awaiting_start = False
                self.reload_requested = False
                return False
            if p.read_int32(self.gate.STATE) == 4 or p.read_int32(0x206324) != 0xFFFFFFFF:
                return False
            if self.hooks.installed and self.hooks.is_current():
                self.connection_warning.refresh(self.ap_connected)
                if p.read_int32(0x206338) != 3:
                    return False
                if self.hooks.entitlement_table is not None and not p.read_int8(self.hooks.entitlement_table + 40):
                    return False
                if self.vendor_catalog is not None:
                    self.vendor_catalog.challenge_level = self.progression.ng_plus if self.progression is not None else 0
                    self.vendor_catalog.sync_cases(self.owned_cases)
                self.hooks.sync_checked(checked)
                self.hooks.sync_entitlements(entitlements)
                if self.skins is not None:
                    self.skins.sync()
                return True
            self._reload_current_level()
            return False
        except Exception:
            self.close()
            raise

    def _reload_current_level(self):
        """Recover missing hooks through a fresh native load, once per attempt."""
        if self.reload_requested:
            return
        p = self.pine
        addresses = (CURRENT_CASE_ADDRESS, FORCE_CASE_ADDRESS, self.gate.STATE, 0x206338)
        state = p.batch_read_int32(addresses)
        module, requested, loader, game = state
        if (module not in CASE_MODULES.values() or requested != 0xFFFFFFFF
                or loader != 5 or game != 3):
            return
        # Never replace travel that began while we were examining the state.
        if p.batch_read_int32(addresses) != state or is_main_menu(p):
            return
        # Mark first: a lost write acknowledgement must not cause repeated reloads.
        self.reload_requested = True
        self.hooks.installed = False
        p.write_int32(FORCE_CASE_ADDRESS, module)
        self.log(f"[SAC] Reloading current level (module {module}) to initialize native checks.")

    def close(self):
        try:
            if (self.hooks.installed and self.pine.get_game_id() == "SCUS-97623"
                    and self.hooks.is_current()
                    and self.pine.read_int32(0x206324) == 0xFFFFFFFF):
                self.connection_warning.refresh(False)
        finally:
            self.gate.release()
            self.starting_case.close()
            self.awaiting_start = False
            self.reload_requested = False

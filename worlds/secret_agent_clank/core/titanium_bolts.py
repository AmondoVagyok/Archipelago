"""Read individual persistent titanium bolt flags, never the spendable total."""
import struct

from ..locations import TITANIUM_BOLT_FLAGS
from .global_flags import GlobalFlags, module_bit, module_counts, read_module_counts


class TitaniumBoltState:
    def __init__(self, pine):
        self.pine = pine
        self.flags = GlobalFlags(pine)
        self.valid = False
        self.reported = set()

    def bind(self, symbols):
        self.valid = False
        if not self.flags.bind(symbols):
            return False
        count_fn = symbols.get("GLOBALVARS_GetTotalTitaniumBoltCount__FUi")
        found_fn = symbols.get("GLOBALVARS_HasTitaniumBoltBeenFound__FUiUi")
        if count_fn is None or found_fn is None:
            return False
        if read_module_counts(self.pine, count_fn) != module_counts(TITANIUM_BOLT_FLAGS):
            return False
        # Validate the native nibble/one-based ID calculation. The JAL's
        # relocated target varies between DLLs; all other words must match.
        code = struct.unpack("<18I", self.pine.read_bytes(found_fn, 72))
        expected = (0x2484FFFF, 0x27BDFFF0, 0x30820001, 0xFFB00000,
                    0x00021080, 0x00042042, 0x00A28021, 0xFFBF0008,
                    0x2610FFFF, 0x24840028, None, 0x320500FF,
                    0x02021006, 0xDFBF0008, 0xDFB00000, 0x30420001,
                    0x03E00008, 0x27BD0010)
        if code[10] >> 26 != 3 or any(
                e is not None and a != e for a, e in zip(code, expected)):
            return False
        self.valid = True
        return True

    def sync(self):
        pass

    def sync_from_ap(self, checked):
        self.reported.update(checked)

    def check(self):
        if not self.valid:
            return []
        flags = self.flags.read(0x28, 15)
        if flags is None:
            return []
        found = {name for name, (module, bit) in TITANIUM_BOLT_FLAGS.items() if module_bit(flags, module, bit)}
        return sorted(found - self.reported)

    def confirm(self, name: str) -> None:
        """Stop reporting `name`; call only once AP has accepted the check."""
        self.reported.add(name)

    @property
    def total(self):
        data = self.flags.read(0x37) if self.valid else None
        return data[0] if data is not None else 0

    def __repr__(self):
        return f"TitaniumBoltState(bound={self.valid}, spendable={self.total})"

"""Persistent Alien Code bits, independently read from native save flags."""
from ...constants.alien_codes import ALIEN_CODE_MODULES, ALIEN_CODES_BY_CASE
from ..global_flags import GlobalFlags, read_module_counts


class AlienCodeInventory:
    def __init__(self, pine):
        self.pine = pine
        self.flags = GlobalFlags(pine)
        self.reported = set()
        self.valid = False
        self.found = set()

    def bind(self, symbols):
        self.valid = False
        if not self.flags.bind(symbols):
            return False
        get_count = symbols.get("GLOBALVARS_GetTotalAlienCodeCount__FUi")
        if get_count is None:
            return False
        if read_module_counts(self.pine, get_count) != dict.fromkeys(ALIEN_CODE_MODULES.values(), 3):
            return False
        self.valid = True
        return True

    def sync(self):
        # Do not baseline away a collection completed during level startup.
        pass

    def sync_from_ap(self, checked):
        self.reported.update(checked)

    def check(self):
        if not self.valid:
            return []
        data = self.flags.read(0x38, 15)
        if data is None:
            return []
        self.found = set()
        for case, module in ALIEN_CODE_MODULES.items():
            for index, name in enumerate(ALIEN_CODES_BY_CASE[case]):
                if data[(module - 1) // 2] & (1 << (((module - 1) & 1) * 4 + index)):
                    self.found.add(name)
        return sorted(self.found - self.reported)

    def confirm(self, name: str) -> None:
        """Stop reporting `name`; call only once AP has accepted the check."""
        self.reported.add(name)

    @property
    def all_found(self):
        return self.valid and len(self.found) == 27

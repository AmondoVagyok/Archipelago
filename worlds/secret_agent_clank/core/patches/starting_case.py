"""SCUS-97623 new-save launch override, confined to the frontend DLL."""
from ...constants import ALL_CASES, CASE_MODULES, SACCases
from ..batch_io import read_blocks, write_blocks
from .asm import Patch, jump, packed, words
from .debug_stubs import DEBUG_STUBS
from .patch import PatchSet


class StartingCase(PatchSet):
    INIT = 0x331700
    CALLS = (0x365F58, 0x3660C4)
    TRAVEL_CALLS = (0x349774, 0x349A30, 0x349E3C)
    CHANGE_LEVEL = 0x330388
    STUBS = (0x338F40, 0x338F70, 0x338FA8, 0x338FD8)
    FRONT_SIGNATURE = packed([0x27BDFFF0, 0x3C030043, 0x2402001E,
                              0xFFBF0000, 0x0C0E3EA6, 0xAC62DE34])
    STUB_WORDS = tuple(tuple(words(stub.signature)) for stub in DEBUG_STUBS)

    def __init__(self, pine, log):
        super().__init__(pine)
        self.log = log
        self.case_name = None  # Older slot data retains the native start.
        self.installed_case = None
        self.patches = []

    def configure(self, slot_data):
        name = slot_data.get("starting_case")
        if name is not None:
            case = next((case for case in ALL_CASES if case.name == name), None)
            if case is None or not slot_data.get("operatives", {}).get(case.operative, 0):
                raise ValueError(f"Invalid or disabled starting case: {name!r}")
        self.case_name = name

    def is_frontend(self):
        return self._frontend_screen() is not None

    def _frontend_screen(self):
        p = self.pine
        travel, state, loading, screen, signature = read_blocks(
            p, [(0x1AAE78, 4), (0x1AAE3C, 4), (0x206324, 4), (0x42DE34, 4), (0x3652C0, len(self.FRONT_SIGNATURE))])
        if ((travel, state, loading) != (packed([0]), packed([5]), packed([0xFFFFFFFF]))
                or signature != self.FRONT_SIGNATURE or p.get_game_id() != "SCUS-97623"):
            return None
        return int.from_bytes(screen, "little")

    def prepare(self, name):
        self.patches = []
        module = CASE_MODULES[name]
        # Case Files uses A9 for Clank in module 4, C8 for Qwark in
        # module 11, and CA for a manually selected case entry.
        clank = int(name == SACCases.ASYANICA_ROOFTOPS)
        qwark = int(name == SACCases.SUCK_AND_JIVE)
        first, second, travel, travel_tail = (address + 8 for address in self.STUBS)
        body1 = [0x27BDFFF0, 0xFFBF0000, 0xFFA40008,
                 jump(self.INIT, True), 0, 0xDFA80008,
                 0x24090000 | module, 0xAD090ECC, jump(second), 0]
        body2 = [0x24090000 | clank, 0xA1090589,
                 0x24090000 | qwark, 0xA10905A8,
                 0x24090001, 0xA10905AA, 0xDFBF0000,
                 0x03E00008, 0x27BD0010]
        # The actual memory-card UI has three New Game exits that hardcode
        # module 1. Its Load Game exit instead reads the saved ECC field;
        # that call (0x349FD8) must remain untouched.
        body3 = [0x3C080042, 0x8D088FD8, 0x24040000 | module,
                 0xAD040ECC, 0x24090000 | clank, 0xA1090589,
                 jump(travel_tail), 0]
        body4 = [0x24090000 | qwark, 0xA10905A8,
                 0x24090001, 0xA10905AA, jump(self.CHANGE_LEVEL), 0]
        edits = []
        for address, original, body in zip(self.STUBS, self.STUB_WORDS, (body1, body2, body3, body4)):
            expected = packed(original)
            replacement = packed([0x03E00008, 0] + body)
            replacement += expected[len(replacement):]
            if len(replacement) != len(expected):
                raise RuntimeError("New-game wrapper exceeds debug stub storage")
            edits.append(Patch(address, expected, replacement))
        for address in self.CALLS:
            edits.append(Patch(address, packed([jump(self.INIT, True), 0x24050001]),
                               packed([jump(first, True), 0x24050001])))
        for address in self.TRAVEL_CALLS:
            edits.append(Patch(address - 4,
                               packed([0x24040001, jump(self.CHANGE_LEVEL, True), 0x24050001]),
                               packed([0x24040001, jump(travel, True), 0x24050001])))
        current = read_blocks(self.pine, [(edit.address, len(edit.original)) for edit in edits])
        for edit, data in zip(edits, current):
            if data != edit.original:
                raise RuntimeError(f"New-game launch layout changed at {edit.address:#x}")
        self.patches = edits
        return edits

    def apply(self):
        if self._frontend_screen() not in (6, 8, 12, 46, 47):
            raise RuntimeError("New-game patches require the idle frontend")
        super().apply()

    def service(self):
        screen = self._frontend_screen()
        if screen is None:
            # DLL storage has been unloaded; never restore stale addresses.
            self.patches.clear()
            self.installed_case = None
            return False
        if self.installed_case == self.case_name:
            return True
        # Install on the menu/intro, before either new-save path runs.
        if screen not in (6, 8, 12, 46, 47):
            return True
        self.close()
        if self.case_name is not None:
            self.prepare(self.case_name)
            try:
                self.apply()
            except Exception:
                self.close()
                raise
            self.installed_case = self.case_name
            self.log(f"[SAC] New saves will start in {self.case_name}. Ready to create a new save.")
        return True

    def close(self):
        if self.patches and self.is_frontend():
            # Remove call sites before reclaiming their bodies.
            edits = list(reversed(self.patches))
            current = read_blocks(self.pine, [(edit.address, len(edit.replacement)) for edit in edits])
            if any(actual not in (edit.replacement, edit.original) for edit, actual in zip(edits, current)):
                raise RuntimeError("New-game hook changed; refusing to overwrite it")
            write_blocks(self.pine, [(edit.address, edit.original)
                                     for edit, actual in zip(edits, current) if actual == edit.replacement])
        self.patches.clear()
        self.installed_case = None

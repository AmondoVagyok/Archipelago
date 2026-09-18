"""Checked writes shared by the native patch experiments.

The caller must keep the affected functions idle during installation/restoration.
Preparing a plan never writes memory. A plan is tied to one loaded module.
"""
from .asm import Patch


class Plan:
    def __init__(self, pine, edits):
        self.pine = pine
        self.edits = tuple(edits)
        self.installed = False
        self.journals = ()
        self.mutable_data = ()
        ranges = sorted((e.address, e.address + len(e.original)) for e in self.edits)
        if any(len(e.original) != len(e.replacement) or not e.original for e in self.edits):
            raise ValueError("Patch length changed")
        if any(a[1] > b[0] for a, b in zip(ranges, ranges[1:])):
            raise ValueError("Overlapping patches")

    def _validate(self, replacement=False):
        if self.pine.get_game_id() != "SCUS-97615":
            raise RuntimeError("Native patches require US PS2 Size Matters (SCUS-97615)")
        for edit in self.edits:
            expected = edit.replacement if replacement else edit.original
            actual = bytearray(self.pine.read_bytes(edit.address, len(expected)))
            if replacement:
                for start, size in self.mutable_data:
                    left, right = max(start, edit.address), min(start + size, edit.address + len(expected))
                    if left < right:
                        lo, hi = left - edit.address, right - edit.address
                        actual[lo:hi] = expected[lo:hi]
                for start, size in self.journals:
                    left, right = max(start, edit.address), min(start + size, edit.address + len(expected))
                    if left < right:
                        lo, hi = left - edit.address, right - edit.address
                        if any(value not in (1, 2, 3) for value in actual[lo:hi]):
                            raise RuntimeError("Native journal was overwritten")
                        actual[lo:hi] = expected[lo:hi]
            if actual != expected:
                raise RuntimeError(f"Native code changed at {edit.address:#x}")

    def install(self):
        self._validate()
        attempted = []
        try:
            for edit in self.edits:
                attempted.append(edit)
                self.pine.write_bytes(edit.address, edit.replacement)
            self._validate(replacement=True)
        except Exception:
            for edit in reversed(attempted):
                self.pine.write_bytes(edit.address, edit.original)
                if self.pine.read_bytes(edit.address, len(edit.original)) != edit.original:
                    raise RuntimeError("Native patch rollback failed")
            raise
        self.installed = True

    def restore(self):
        self._validate(replacement=True)
        for edit in reversed(self.edits):
            self.pine.write_bytes(edit.address, edit.original)
        self._validate()
        self.installed = False

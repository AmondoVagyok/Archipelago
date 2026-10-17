"""Lifecycle for one prepared native patch."""
from abc import ABC, abstractmethod

from ..batch_io import read_blocks, write_blocks


class Patch(ABC):
    def __init__(self, pine):
        self.pine = pine
        self.address = None
        self.original = b""
        self.replacement = b""

    @abstractmethod
    def prepare(self, **kwargs):
        """Validate inputs and capture original bytes without changing RAM."""
        raise NotImplementedError

    def apply(self):
        """Write a prepared patch, verify it, and undo a failed write."""
        if self.address is None or not self.replacement:
            raise RuntimeError("Prepare the patch before applying it")
        if self.pine.read_bytes(self.address, len(self.original)) != self.original:
            raise RuntimeError("Code changed since patch preparation")
        try:
            self.pine.write_bytes(self.address, self.replacement)
            if self.pine.read_bytes(self.address, len(self.replacement)) != self.replacement:
                raise RuntimeError("Patch readback failed")
        except Exception as err:
            self.pine.write_bytes(self.address, self.original)
            if self.pine.read_bytes(self.address, len(self.original)) != self.original:
                raise RuntimeError("Patch rollback readback failed") from err
            raise

    @abstractmethod
    def read(self):
        """Read the runtime data associated with this patch without changing it."""
        raise NotImplementedError


class PatchSet(Patch):
    """A routine whose code and call sites require several coordinated writes."""

    def __init__(self, pine):
        super().__init__(pine)
        self.patches = []

    def apply(self):
        """Apply the complete prepared set while native execution is held."""
        if not self.patches:
            raise RuntimeError("Prepare a nonempty patch set before applying it")
        if not self._matches("original"):
            raise RuntimeError("Code changed since patch preparation")
        try:
            write_blocks(self.pine, [(patch.address, patch.replacement) for patch in self.patches])
            if not self._matches("replacement"):
                raise RuntimeError("Patch readback failed")
        except Exception as err:
            write_blocks(self.pine, [(patch.address, patch.original) for patch in reversed(self.patches)])
            if not self._matches("original"):
                raise RuntimeError("Patch rollback readback failed") from err
            raise

    def _matches(self, field):
        expected = [getattr(patch, field) for patch in self.patches]
        current = read_blocks(self.pine, [(patch.address, len(data)) for patch, data in zip(self.patches, expected)])
        return current == expected

    def read(self):
        """Read patched sites for diagnostics; code-only routines have no table."""
        current = read_blocks(self.pine, [(patch.address, len(patch.replacement)) for patch in self.patches])
        return {patch.address: data for patch, data in zip(self.patches, current)}

"""Generic unlocked-item tracker, reused for Ratchet's weapons, Clank's spy
gadgets, and Qwark's items alike -- each is just a name -> "unlocked flag
address" table (see core/address_maps/ps2.py's CaseAddresses), so one
implementation covers all three characters' inventories instead of three
near-duplicate classes.

Addresses are per-case, not fixed -- rebound via set_addrs() on every case
load (see core/planets.py's CaseInventory.set_case())."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...pypine import Pine


class ItemInventory:

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine
        self.item_addrs: dict[str, int] = {}
        self.owned: dict[str, bool] = {}

    def set_addrs(self, item_addrs: dict[str, int] | None) -> None:
        self.item_addrs = dict(item_addrs or {})
        self.owned = dict.fromkeys(self.item_addrs, False)

    def get(self, name: str) -> bool:
        addr = self.item_addrs.get(name)
        if addr is None:
            return False
        return bool(self.pine.read_int8(addr))

    def set(self, name: str, unlocked: bool) -> None:
        addr = self.item_addrs.get(name)
        if addr is None:
            return
        self.pine.write_int8(addr, 1 if unlocked else 0)

    def strip_all(self) -> None:
        """Zero every tracked item's unlocked bit. Called on death and on
        every case transition (see core/core.py's Core._strip_all_inventories)
        so a stale/leftover bit from the previous case is never left
        showing before apply_all() re-grants true AP ownership once the new
        case is ready."""
        for name in self.item_addrs:
            self.set(name, False)
        self.owned = dict.fromkeys(self.item_addrs, False)

    def apply_all(self, ap_owned: dict[str, bool]) -> None:
        """Write true AP ownership for every tracked item."""
        for name in self.item_addrs:
            owned = ap_owned.get(name, False)
            if self.owned.get(name) != owned:
                self.set(name, owned)
            self.owned[name] = owned

    def check(self) -> list[str]:
        """Diff current raw memory against the last-known owned state,
        returning item names that flipped 0 -> 1 since the last call (i.e.
        purchased/picked-up this tick)."""
        changed: list[str] = []
        for name in self.item_addrs:
            now = self.get(name)
            if now and not self.owned.get(name, False):
                changed.append(name)
            self.owned[name] = now
        return changed

    def __repr__(self) -> str:
        return f"ItemInventory(items={len(self.item_addrs)})"

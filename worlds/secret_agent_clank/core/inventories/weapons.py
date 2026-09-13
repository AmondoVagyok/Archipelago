"""Ratchet's WeaponData table -- the single 40-slot struct array that backs
every weapon/tool/wrench-ability Ratchet can carry during SAC's Ratchet
action sections (see constants/weapons.py's RATCHET_WEAPONS docstring for
the separate, still-placeholder vendor-order list this does NOT replace).

Reverse-engineered via Ghidra/PINE (see docs/ for the write-up): each
struct is WEAPON_STRUCT_SIZE (0x74/116) bytes, back to back, 40 entries per
array. WEAPON_ORDER below is that struct array's own slot order (index ==
slot id), pulled straight from the table's name pointers -- slot 0 is
always blank (no name pointer, category 0) and slot 1 is a real weapon
category (2) with no name pointer ever observed (unknown/unnamed), so both
are None. Every other slot's string is the exact internal name the game
itself uses (read live out of the name-pointer strings), not a made-up
display name.

Planet/case model
------------------
Like every other per-case address in core/address_maps/ps2.py, the array's
base address moves every time a different case is loaded (SAC streams each
case's Ratchet-gameplay code+data in as its own SN-Systems SNDLL module --
see docs/), while the struct's internal field offsets stay fixed. So this
module never hardcodes an address: set_base() rebinds every weapon to the
newly-loaded case's array_base (or unbinds entirely when array_base is
None), the same way core/planets.py's CaseInventory.set_case() rebinds
everything else -- see core/address_maps/ps2.py's CaseAddresses.weapon_array
and core/planets.py's set_case() call into WeaponInventory.set_base().

Batched I/O
-----------
check()/apply_all()/strip_all() are the drop-in replacement for
core/inventory.py's ItemInventory (same method names/signatures, so
core/core.py's existing call sites don't change) but read/write every bound
weapon's owned flag in ONE pine.batch_read_int32()/batch_write_int32() call
instead of looping one weapon at a time -- see rac_size_matters/core/
weapons.py's WeaponInventory.check() for the pattern this mirrors.
read_ammo()/write_ammo() are the same batched shape, exposed separately so
a future ammo-sync client (mirroring rac_size_matters/client/ammo_link.py)
has a ready-made batched read/write pair to build on, without this module
needing to know anything about the network side.
"""
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...pypine import Pine

# --- Struct layout (see docs/ for the full field write-up; only the two
# fields this module actually tracks are given names here) -----------------
WEAPON_STRUCT_SIZE: int = 0x74  # 116 bytes per entry, 40 entries per array

_OFFSET_NAME_PTR     = 0x00  # char* -- not read live here, only used to derive WEAPON_ORDER once
_OFFSET_CATEGORY     = 0x04  # int -- 2=Ratchet weapon, 1=Ratchet tool/item, 3=wrench ability (not read live here)
_OFFSET_CURRENT_AMMO = 0x60  # int32 -- current ammo/charge count
_OFFSET_OWNED_FLAG   = 0x70  # int32 -- 0 = not picked up yet, nonzero = owned

# --- Mod-install flags (CONFIRMED via a clean live before/after byte diff of
# the entire 40-slot table across a real in-game vendor mod purchase -- see
# docs/) -----------------------------------------------------------------
# One byte per mod slot, 3 slots per weapon. A weapon-mod purchase in
# SCRNMODVENDOR (see FUN_003d42b0 -> FUN_0035c3d8 in the Ghidra decompile)
# writes 1 to *(byte*)(GadgetData_base + slot + 0x68) once the mod is
# installed -- this table IS that GadgetData layout, not a separate struct.
# Live evidence: bought one weapon mod, bolts dropped by exactly 15000 (a
# different, smaller price than the flat 35000 charged for a bare weapon
# unlock), and diffing a before/after snapshot of the ENTIRE 4640-byte
# table found exactly one changed byte in the whole array: slot 9
# ("minelauncher"), struct offset 0x69, 0x00 -> 0x01 -- i.e. mod slot 1
# (0x68 + 1) for that weapon. Every other byte in every other slot was
# byte-for-byte identical before and after.
_OFFSET_MOD_SLOTS = 0x68  # 3 consecutive bytes: mod slot 0/1/2 installed-flags
MOD_SLOT_COUNT    = 3

# Positional slot order (index == raw weapon-table slot id). None = blank
# slot (0) or a slot with no name ever observed in-game (1) -- neither gets
# a WeaponAddresses entry from build_weapons() below, matching
# rac_size_matters/core/weapons.py's `if name is not None` filtering.
WEAPON_ORDER: list[str | None] = [
    None,                          # slot 0   blank
    None,                          # slot 1   unknown/unnamed (category 2, no name)
    "blaster",                     # slot 2
    "shardgun",                    # slot 3
    "beemineglove",                # slot 4
    "shockrocket",                 # slot 5
    "walloper",                    # slot 6
    "plasmawhip",                  # slot 7
    "porkbomb",                    # slot 8
    "minelauncher",                # slot 9
    "ryno",                        # slot 10
    "throwTie",                    # slot 11
    "CuffLink",                    # slot 12
    "TangleVine",                  # slot 13
    "HoloKnuckles",                # slot 14
    "FlamethrowerPen",             # slot 15
    "LightningUmbrella",           # slot 16
    "fountainpen",                 # slot 17
    "hypnowatch",                  # slot 18
    "QwarkBlaster",                # slot 19
    "Vacuum",                      # slot 20
    "GiantQwarkBlaster",           # slot 21
    "hypershot",                   # slot 22   category 1 (tool/item, not a weapon)
    "ratchetpda",                  # slot 23   category 1
    "holomonocle",                 # slot 24   category 1
    "sunglasses",                  # slot 25   category 1
    "clankpda",                    # slot 26   category 1
    "bolttransfer",                # slot 27   category 3 (wrench ability)
    "wrenchpower_firebomb",        # slot 28   category 3
    "wrenchpower_triplewave",      # slot 29   category 3
    "wrenchpower_crystallix",      # slot 30   category 3
    "wrenchpower_wildburst",       # slot 31   category 3
    "jetboots",                    # slot 32   category 3
    "omnikey",                     # slot 33   category 3
    "mapomatic",                   # slot 34   category 3
    "boltgrabber",                 # slot 35   category 3
    "boxbreaker",                  # slot 36   category 3
    "superkick",                   # slot 37   category 3
    "kickblast",                   # slot 38   category 3
    "kicksplosion",                # slot 39   category 3
]

# One member per named WEAPON_ORDER slot (the two None/blank slots have no
# member) -- built directly from WEAPON_ORDER itself so a member can never
# drift out of sync with the string it names. Lets callers write
# WeaponSlot.SHOCKROCKET instead of retyping "shockrocket" by hand (see
# patches/locations.py's VENDOR_LOCATIONS/PICKUP_LOCATIONS, previously the
# same internal names typed out a second time with nothing tying the two
# copies together).
WeaponSlot = IntEnum(
    "WeaponSlot", {name.upper(): index for index, name in enumerate(WEAPON_ORDER) if name is not None},
)


class WeaponInt32Field:
    """Descriptor for a 4-byte int field at a fixed offset within a
    WeaponAddresses instance's struct entry. Every read/write here is a
    single, un-batched pine call -- use WeaponInventory's batched
    check()/apply_all()/strip_all()/read_ammo()/write_ammo() instead of this
    for anything touching more than one weapon at a time."""
    __slots__ = ("offset",)

    def __init__(self, offset: int) -> None:
        self.offset = offset

    def __get__(self, instance: "WeaponAddresses | None", owner: object = None) -> int:
        if instance is None:
            return self  # type: ignore[return-value]
        return instance.pine.read_int32(instance.base + self.offset)

    def __set__(self, instance: "WeaponAddresses", value: int) -> None:
        instance.pine.write_int32(instance.base + self.offset, value)


class WeaponAddresses:
    """One weapon's live struct entry. base is that weapon's own
    array_base + slot_index * WEAPON_STRUCT_SIZE -- see build_weapons()."""

    ammo  = WeaponInt32Field(_OFFSET_CURRENT_AMMO)
    owned = WeaponInt32Field(_OFFSET_OWNED_FLAG)

    def __init__(self, base: int, pine: "Pine") -> None:
        self.base = base
        self.pine = pine

    def mod_installed(self, slot: int) -> bool:
        """True if mod slot `slot` (0/1/2) is installed on this weapon --
        see _OFFSET_MOD_SLOTS above."""
        if not (0 <= slot < MOD_SLOT_COUNT):
            raise ValueError(f"mod slot must be 0-{MOD_SLOT_COUNT - 1}, got {slot}")
        return bool(self.pine.read_int8(self.base + _OFFSET_MOD_SLOTS + slot))

    def grant_mod(self, slot: int) -> None:
        """Directly write the installed flag for mod slot `slot` (0/1/2) --
        the same write SCRNMODVENDOR's purchase flow performs after
        deducting bolts (see _OFFSET_MOD_SLOTS docstring), minus the
        purchase. No bolts are spent."""
        if not (0 <= slot < MOD_SLOT_COUNT):
            raise ValueError(f"mod slot must be 0-{MOD_SLOT_COUNT - 1}, got {slot}")
        self.pine.write_int8(self.base + _OFFSET_MOD_SLOTS + slot, 1)

    def __repr__(self) -> str:
        return f"WeaponAddresses(base=0x{self.base:X})"


def build_weapons(array_base: int | None, pine: "Pine") -> dict[str, WeaponAddresses]:
    """Bind every named slot in WEAPON_ORDER to its live struct entry.
    Returns {} when array_base is None (no case loaded / unrecognized case)
    -- mirrors rac_size_matters/core/weapons.py's build_weapons() exactly,
    including skipping every None slot rather than creating all 40."""
    if array_base is None:
        return {}
    weapons: dict[str, WeaponAddresses] = {}
    for i, name in enumerate(WEAPON_ORDER):
        if name is not None:
            weapons[name] = WeaponAddresses(array_base + i * WEAPON_STRUCT_SIZE, pine)
    return weapons


class WeaponInventory:
    """Drop-in replacement for core/inventory.py's ItemInventory, scoped to
    Ratchet's WeaponData-table weapons -- same check()/apply_all()/
    strip_all() method names and signatures as ItemInventory, so
    core/core.py and core/planets.py don't need any call-site changes
    beyond constructing this instead and calling set_base() instead of
    set_addrs(). The difference is entirely internal: every weapon lives in
    one contiguous struct array, so all I/O below is batched across every
    bound weapon in a single pine call instead of looping one address at a
    time.

    Planet/case-dependent: call set_base(array_base) whenever the loaded
    case changes (see core/planets.py's CaseInventory.set_case(), which
    passes CaseAddresses.weapon_array)."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine
        self.weapons: dict[str, WeaponAddresses] = {}
        # Last-known owned state (0/1), used by check() to detect 0->1
        # flips without re-reading every weapon serially.
        self._raw_owned: dict[str, int] = {}
        # Last-known mod-slot state ([0/1, 0/1, 0/1] per weapon), used by
        # check_mods() the same way _raw_owned is used by check().
        self._raw_mods: dict[str, list[int]] = {}

    def set_base(self, array_base: int | None) -> None:
        """Rebind every weapon to the newly-loaded case's array base, or
        unbind entirely when array_base is None (unrecognized/no case)."""
        self.weapons = build_weapons(array_base, self.pine)
        self._raw_owned = dict.fromkeys(self.weapons, 0)
        self._raw_mods = {name: [0] * MOD_SLOT_COUNT for name in self.weapons}

    # -- Single-weapon convenience accessors (not batched -- fine for
    # one-off reads/writes, e.g. from a debug command) ----------------------

    def has_weapon(self, name: str) -> bool:
        w = self.weapons.get(name)
        return bool(w.owned) if w is not None else False

    def get_ammo(self, name: str) -> int:
        w = self.weapons.get(name)
        return w.ammo if w is not None else 0

    def set_ammo(self, name: str, value: int) -> None:
        w = self.weapons.get(name)
        if w is not None:
            w.ammo = value

    # -- Batched unlock tracking (ItemInventory-compatible) -----------------

    def strip_all(self) -> None:
        """Batched zero of every bound weapon's owned flag. Called on death
        and at the start of every case transition (see core/core.py's
        Core._strip_all_inventories()) so a stale bit from the previous
        case's memory is never shown before apply_all() re-grants true AP
        ownership once the new case is ready."""
        if not self.weapons:
            return
        ops = [(w.base + _OFFSET_OWNED_FLAG, 0) for w in self.weapons.values()]
        self.pine.batch_write_int32(ops)
        self._raw_owned = dict.fromkeys(self.weapons, 0)

    def apply_all(self, ap_owned: dict[str, bool]) -> None:
        """Batched write of true AP ownership for every bound weapon."""
        if not self.weapons:
            return
        ops = [
            (w.base + _OFFSET_OWNED_FLAG, 1 if ap_owned.get(name, False) else 0)
            for name, w in self.weapons.items() if name in ap_owned
        ]
        self.pine.batch_write_int32(ops)
        self._raw_owned.update({name: int(bool(value)) for name, value in ap_owned.items() if name in self.weapons})

    def sync(self) -> None:
        """Baseline a newly bound table without inventing pickup events."""
        if self.weapons:
            values = self.pine.batch_read_int32([w.base + _OFFSET_OWNED_FLAG for w in self.weapons.values()])
            self._raw_owned = {name: int(bool(value)) for name, value in zip(self.weapons, values)}

    def check(self) -> list[str]:
        """Batched read of every bound weapon's owned flag, diffed against
        the last-known state. Returns weapon names that flipped 0 -> 1
        since the last call (i.e. picked up in-game this tick) -- same
        return shape as ItemInventory.check(), so core/core.py's
        `for name in self.case.ratchet_items.check(): self.send_location(name)`
        keeps working unchanged."""
        if not self.weapons:
            return []
        names = list(self.weapons)
        addrs = [self.weapons[name].base + _OFFSET_OWNED_FLAG for name in names]
        values = self.pine.batch_read_int32(addrs)
        changed: list[str] = []
        for name, value in zip(names, values):
            owned = 1 if value else 0
            if owned and not self._raw_owned.get(name):
                changed.append(name)
            self._raw_owned[name] = owned
        return changed

    def check_mods(self) -> list[tuple[str, int]]:
        """Batched read of every bound weapon's 3 mod-slot flags
        (_OFFSET_MOD_SLOTS), diffed against last-known state. Returns
        (weapon_name, slot) pairs that flipped 0 -> 1 since the last call
        -- i.e. a weapon mod purchased/installed in-game this tick. Mirrors
        check()'s shape/semantics but one level more granular (per mod slot
        instead of per weapon). Uses individual reads (not yet a single
        batch call across all 3*N bytes) since this is new/lightly-used
        compared to the hot owned-flag path."""
        if not self.weapons:
            return []
        changed: list[tuple[str, int]] = []
        for name, w in self.weapons.items():
            prev = self._raw_mods.get(name, [0] * MOD_SLOT_COUNT)
            cur = [self.pine.read_int8(w.base + _OFFSET_MOD_SLOTS + s) for s in range(MOD_SLOT_COUNT)]
            for slot, (p, c) in enumerate(zip(prev, cur)):
                if c and not p:
                    changed.append((name, slot))
            self._raw_mods[name] = cur
        return changed

    # -- Batched ammo I/O (for a future ammo-sync client, and for AP's own
    # ammo-count restore/consumable handling if that's ever added) ----------

    def read_ammo(self) -> dict[str, int]:
        """Batched read of every currently-OWNED weapon's ammo. Owned-only
        mirrors rac_size_matters/client/ammo_link.py's AmmoLinkMixin, which
        only mirrors ammo for weapons the player actually has."""
        owned_names = [name for name in self.weapons if self._raw_owned.get(name)]
        if not owned_names:
            return {}
        addrs = [self.weapons[name].base + _OFFSET_CURRENT_AMMO for name in owned_names]
        values = self.pine.batch_read_int32(addrs)
        return dict(zip(owned_names, values))

    def write_ammo(self, ammo: dict[str, int]) -> None:
        """Batched write of ammo values, restricted to weapons that are both
        currently bound (this case's array) and currently owned -- silently
        drops anything else rather than raising, since an incoming
        cross-player ammo-sync payload can legitimately reference a weapon
        this player hasn't picked up yet on this case."""
        ops = [
            (self.weapons[name].base + _OFFSET_CURRENT_AMMO, value)
            for name, value in ammo.items()
            if name in self.weapons and self._raw_owned.get(name)
        ]
        if ops:
            self.pine.batch_write_int32(ops)

    def __repr__(self) -> str:
        return f"WeaponInventory(weapons={len(self.weapons)})"

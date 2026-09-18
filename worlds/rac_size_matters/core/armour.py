from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum, IntFlag
from typing import NamedTuple

from ..constants import (
    Rac5ClankChallenges,
    Rac5Locations,
    Rac5Planets,
    Rac5SkyboardChallenges,
)
from ..pypine import Pine
from .address_maps import ARMOUR_BASE
from .states.base_state import BaseState

_BOOTS_MASK = 0xF0


class ArmourSet(IntEnum):
    """Value set in armour slots to represent what armour is currently equiped."""

    Wildfire = 1
    Sludge = 2
    Crystallix = 3
    Electroshock = 4
    MegaBomb = 5
    Hyperborean = 6
    Chameleon = 7


class ArmourPiece(IntFlag):
    """Armour pieces are bits in a byte: chestplate 0x01, helmet 0x02, gloves 0x04,
    boots 0x10 (any value with bit 4 set counts as boots equipped)."""

    NONE = 0
    CHESTPLATE = 0x01
    HELMET = 0x02
    GLOVES = 0x04
    BOOTS = 0x10
    ALL = 0x17

    @classmethod
    def from_raw(cls, value: int) -> ArmourPiece:
        """Normalize raw value of armour piece because boots are represented by any value with bit 4 set"""
        normalized = value & 0x0F
        if value & _BOOTS_MASK:
            normalized |= cls.BOOTS
        return cls(normalized)


@dataclass
class ArmourSnapshot:
    """Snapshot of the player's armour state at a given point in time. Any field left as
    None is treated as unset — ArmourStruct.write() skips it and leaves memory untouched."""

    chestplate: ArmourSet | None = None
    helmet: ArmourSet | None = None
    gloves_left: ArmourSet | None = None
    gloves_right: ArmourSet | None = None
    boots_left: ArmourSet | None = None
    boots_right: ArmourSet | None = None
    wildfire: ArmourPiece | None = None
    sludge: ArmourPiece | None = None
    crystallix: ArmourPiece | None = None
    electroshock: ArmourPiece | None = None
    mega_bomb: ArmourPiece | None = None
    hyperborean: ArmourPiece | None = None
    chameleon: ArmourPiece | None = None

    def owned_mask(self) -> int:
        """Bitmask with one bit per armour set (bit i = ArmourStruct.SET_FIELDS order)
        that has any piece owned. None/NONE fields count as not-owned."""
        return sum(1 << i for i, name in enumerate(ArmourStruct.SET_FIELDS) if getattr(self, name))


class ArmourStruct:
    """Batched pine read/write over the full armour block. BASE_ADDRESS is fixed —
    it doesn't move between planets/levels, so this lives alongside the rest of the
    armour logic instead of the per-planet memory structs."""

    BASE_ADDRESS = ARMOUR_BASE
    pine: Pine | None = None
    GameState: ArmourSnapshot | None = None

    _fields_ = [
        ("chestplate",   Pine.DataSize.INT8),
        ("helmet",       Pine.DataSize.INT8),
        ("gloves_left",  Pine.DataSize.INT8),
        ("gloves_right", Pine.DataSize.INT8),
        ("boots_left",   Pine.DataSize.INT8),
        ("boots_right",  Pine.DataSize.INT8),
        ("wildfire",     Pine.DataSize.INT8),
        ("sludge",       Pine.DataSize.INT8),
        ("crystallix",   Pine.DataSize.INT8),
        ("electroshock", Pine.DataSize.INT8),
        ("mega_bomb",    Pine.DataSize.INT8),
        ("hyperborean",  Pine.DataSize.INT8),
        ("chameleon",    Pine.DataSize.INT8),
    ]

    SLOT_FIELDS: tuple[str, ...] = (
        "chestplate", "helmet", "gloves_left", "gloves_right", "boots_left", "boots_right",
    )
    SET_FIELDS: tuple[str, ...] = (
        "wildfire", "sludge", "crystallix", "electroshock", "mega_bomb", "hyperborean", "chameleon",
    )

    @classmethod
    def _iter_fields(cls):
        """Yield (name, size, address) for each field, laid out back-to-back from BASE_ADDRESS."""
        offset = 0
        for name, size in cls._fields_:
            yield name, size, cls.BASE_ADDRESS + offset
            offset += size

    def read(self) -> None:
        """Batched read of every field, decoded the same way the old per-field
        descriptors did: a slot is None when unequipped (raw 0) or the matching
        ArmourSet otherwise; a set is always an ArmourPiece, boots-bit normalized."""
        fields = list(self._iter_fields())
        values = self.pine.batch_read([(size, address) for _, size, address in fields])
        decoded = {}
        for (name, _, _), raw in zip(fields, values):
            if name in self.SLOT_FIELDS:
                decoded[name] = ArmourSet(raw) if raw else None
            else:
                decoded[name] = ArmourPiece.from_raw(raw)
        self.GameState = ArmourSnapshot(**decoded)

    def write(self, snapshot: ArmourSnapshot) -> None:
        """Write only the fields set on `snapshot` — unset (None) fields are left untouched in memory."""
        writes = [
            (size, address, self.pine.to_bytes(int(value), size))
            for name, size, address in self._iter_fields()
            if (value := getattr(snapshot, name)) is not None
        ]
        self.pine.batch_write(writes)


class ArmourPickup(NamedTuple):
    set_key: str
    piece: ArmourPiece
    name: str
    planet: str


EQUIPPED_SLOT_TO_PIECE: dict[str, ArmourPiece] = {
    "chestplate": ArmourPiece.CHESTPLATE,
    "helmet": ArmourPiece.HELMET,
    "gloves_left": ArmourPiece.GLOVES,
    "gloves_right": ArmourPiece.GLOVES,
    "boots_left": ArmourPiece.BOOTS,
    "boots_right": ArmourPiece.BOOTS,
}

ARMOUR_PICKUPS: list[ArmourPickup] = [
    ArmourPickup("wildfire", ArmourPiece.CHESTPLATE, Rac5Locations.POKITARU_CHESTPLATE, Rac5Planets.POKITARU),
    ArmourPickup("wildfire", ArmourPiece.GLOVES, Rac5Locations.POKITARU_GLOVES, Rac5Planets.POKITARU),
    ArmourPickup("sludge", ArmourPiece.BOOTS, Rac5Locations.RYLLUS_BOOTS, Rac5Planets.RYLLUS),
    ArmourPickup("wildfire", ArmourPiece.HELMET, Rac5Locations.RYLLUS_HELMET, Rac5Planets.RYLLUS),
    ArmourPickup("sludge", ArmourPiece.CHESTPLATE, Rac5Locations.KALIDON_CHESTPLATE, Rac5Planets.KALIDON),
    ArmourPickup("wildfire", ArmourPiece.BOOTS, Rac5Locations.KALIDON_BOOTS, Rac5Planets.KALIDON),
    ArmourPickup("crystallix", ArmourPiece.CHESTPLATE, Rac5Locations.DREAMTIME_CHESTPLATE, Rac5Planets.DREAMTIME),
    ArmourPickup("crystallix", ArmourPiece.BOOTS, Rac5Locations.OUTPOST_OMEGA_BOOTS, Rac5Planets.OUTPOST_OMEGA),
    ArmourPickup("electroshock", ArmourPiece.HELMET, Rac5Locations.CHALLAX_HELMET, Rac5Planets.CHALLAX),
    ArmourPickup("mega_bomb", ArmourPiece.HELMET, Rac5Locations.DAYNI_MOON_HELMET, Rac5Planets.DAYNI_MOON),
    ArmourPickup("mega_bomb", ArmourPiece.CHESTPLATE, Rac5Locations.INSIDE_CLANK_CHESTPLATE, Rac5Planets.INSIDE_CLANK),

    ArmourPickup("electroshock", ArmourPiece.GLOVES, Rac5Locations.METALIS_GLOVES, Rac5Planets.METALIS),
    ArmourPickup("electroshock", ArmourPiece.CHESTPLATE, Rac5Locations.CHALLAX_CHESTPLATE, Rac5Planets.CHALLAX),

    ArmourPickup("hyperborean", ArmourPiece.GLOVES, Rac5Locations.POKITARU_HYPERBOREAN_GLOVES, Rac5Planets.POKITARU),
    ArmourPickup("hyperborean", ArmourPiece.BOOTS, Rac5Locations.RYLLUS_HYPERBOREAN_BOOTS, Rac5Planets.RYLLUS),
    ArmourPickup(
        "hyperborean", ArmourPiece.CHESTPLATE,
        Rac5Locations.DREAMTIME_HYPERBOREAN_CHESTPLATE, Rac5Planets.DREAMTIME,
    ),
    ArmourPickup("hyperborean", ArmourPiece.HELMET, Rac5Locations.CHALLAX_HYPERBOREAN_HELMET, Rac5Planets.CHALLAX),
    ArmourPickup("chameleon", ArmourPiece.BOOTS, Rac5Locations.POKITARU_CHAMELEON_BOOTS, Rac5Planets.POKITARU),
    ArmourPickup("chameleon", ArmourPiece.CHESTPLATE, Rac5Locations.KALIDON_CHAMELEON_CHESTPLATE, Rac5Planets.KALIDON),
    ArmourPickup(
        "chameleon", ArmourPiece.GLOVES,
        Rac5Locations.OUTPOST_OMEGA_CHAMELEON_GLOVES, Rac5Planets.OUTPOST_OMEGA,
    ),
    ArmourPickup(
        "chameleon", ArmourPiece.HELMET,
        Rac5Locations.INSIDE_CLANK_CHAMELEON_HELMET, Rac5Planets.INSIDE_CLANK,
    ),
]

ARMOUR_FLAG_TO_LOCATION: dict[tuple[str, ArmourPiece], str] = {(ap.set_key, ap.piece): ap.name for ap in ARMOUR_PICKUPS}

CHALLENGE_LOCATION_TO_ARMOUR_FLAG: dict[str, tuple[str, ArmourPiece]] = {
    Rac5ClankChallenges.METALIS_REVENGE: ("crystallix", ArmourPiece.HELMET),
    Rac5ClankChallenges.METALIS_UBER: ("crystallix", ArmourPiece.GLOVES),
    Rac5ClankChallenges.METALIS_NIGHT: ("sludge", ArmourPiece.GLOVES),
    Rac5ClankChallenges.DAYNI_MOON_SHOWDOWN: ("mega_bomb", ArmourPiece.GLOVES),
    Rac5ClankChallenges.DAYNI_MOON_INFINITE: ("mega_bomb", ArmourPiece.BOOTS),
    Rac5SkyboardChallenges.OUTPOST_OMEGA_VERTIGO: ("electroshock", ArmourPiece.BOOTS),
}




class ArmourInventory(BaseState):
    """Owns a single ArmourStruct plus two logical states: ap_armour (what AP has
    granted -- the only thing that actually counts as "owned") and game_armour
    (what's been physically picked up in this playthrough, regardless of AP
    ownership). Kept separate on purpose: with ArmourSpawnGate bypassing vanilla's
    story/challenge-mode gate, every pickup manifests whether or not it's actually
    yours, so a piece being in game_armour must NEVER by itself grant it in-game --
    only ap_armour does that (see apply_full()). game_armour exists so
    check()/restore_armour_from_locations() don't keep re-reporting the same
    physically-found-but-not-(yet)-AP-owned pickup every tick, and it's also what
    the transient death-sequence display (apply_collected_only()) shows on its own,
    independent of AP ownership -- see that method for why."""

    def __init__(self, pine: Pine) -> None:
        super().__init__()
        self.pine = pine
        self.struct = ArmourStruct()
        self.struct.pine = pine
        self.ap_armour: ArmourSnapshot = ArmourSnapshot()
        self.game_armour: ArmourSnapshot = ArmourSnapshot()

    def read(self) -> ArmourSnapshot:
        """Batched read of the full armour block."""
        self.struct.read()
        return self.struct.GameState

    def sync_equipped(self, data: dict[str, int]) -> None:
        """Write an Archipelago data-storage dict into the equipped slots."""
        fields = {name: int(value) for name, value in data.items() if name in ArmourStruct.SLOT_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def set_ap_armour(self, data: dict[str, int]) -> None:
        """Replace ap_armour wholesale (not a merge) from an AP data-storage dict.
        Pure bookkeeping; call apply_full()/apply_collected_only() to write."""
        fields = {
            name: ArmourPiece.from_raw(int(value))
            for name, value in data.items() if name in ArmourStruct.SET_FIELDS
        }
        self.ap_armour = ArmourSnapshot(**fields)

    def record_pickup(self, pieces: dict[str, ArmourPiece]) -> None:
        """OR-merge newly detected in-game pickups into game_armour -- purely so
        check() doesn't re-report the same not-(yet)-AP-owned pickup forever. Does NOT
        by itself grant anything in-game; see the class docstring. Pure bookkeeping,
        no memory write."""
        merged = {
            name: (getattr(self.game_armour, name) or ArmourPiece.NONE) | piece
            for name, piece in pieces.items()
        }
        self.game_armour = replace(self.game_armour, **merged)

    def check(self) -> dict[str, ArmourPiece]:
        """Every-tick diff, titanium-bolt style: read raw memory and return whatever
        bits aren't already accounted for by ap_armour or game_armour, per set --
        i.e. "has this pickup been reported before", not "is it owned". A piece
        found here that isn't in ap_armour is reported via record_pickup() so it
        isn't reported again, but is NOT thereby granted in-game: apply_full() only
        ever applies ap_armour, so the very next call re-locks it back to unowned
        unless/until the matching AP item actually comes back. ArmourSpawnGate lets
        an unowned piece keep re-manifesting and being "found" again for as long as
        its location stays unresolved in the player's favor, same as a
        not-yet-owned weapon vendor slot."""
        current = self.read()
        new_pieces: dict[str, ArmourPiece] = {}
        for name in ArmourStruct.SET_FIELDS:
            raw = int(getattr(current, name) or 0)
            known = int(getattr(self.ap_armour, name) or 0) | int(getattr(self.game_armour, name) or 0)
            new_bits = raw & ~known
            if new_bits:
                new_pieces[name] = ArmourPiece(new_bits)
        if new_pieces:
            self.record_pickup(new_pieces)
        return new_pieces

    def apply_full(self) -> None:
        """Write ap_armour to memory — only what AP has actually granted. Deliberately
        NOT OR'd with game_armour: a piece the player physically found but doesn't
        (yet) own via AP must not stick around just because it was found, exactly like
        an unowned weapon/gadget vendor "purchase" gets re-locked — see the class
        docstring for why this matters now that ArmourSpawnGate lets any pickup
        manifest regardless of ownership."""
        fields = {name: (getattr(self.ap_armour, name) or ArmourPiece.NONE) for name in ArmourStruct.SET_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def apply_collected_only(self) -> None:
        """Write only game_armour — death-sequence state: shows exactly what's been
        physically found in this playthrough, regardless of AP ownership (deliberately
        NOT filtered by ap_armour, unlike apply_full() — this is a transient display
        during the death sequence, not persistent ownership; _handle_respawn()'s
        apply_full() call corrects everything back to AP truth immediately after).
        Every field is written explicitly to avoid stale values."""
        fields = {name: (getattr(self.game_armour, name) or ArmourPiece.NONE) for name in ArmourStruct.SET_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def clear_unlocked(self) -> None:
        """Zero every unlocked-set byte in memory to open a clean 0->1 pickup-detection
        window; never touches ap_armour/game_armour."""
        self.struct.write(ArmourSnapshot(**dict.fromkeys(ArmourStruct.SET_FIELDS, ArmourPiece.NONE)))

    def __repr__(self) -> str:
        return f"ArmourInventory(ap={self.ap_armour!r}, game={self.game_armour!r})"


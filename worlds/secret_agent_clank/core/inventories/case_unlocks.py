"""Per-case unlock gate. Every case's locked/unlocked byte lives in one
table -- but that table's absolute location in memory moves every time
the player loads a different case (CONFIRMED live: reading the same
absolute address again after transitioning to a different case, with no
intervening savestate reload, returns code/unrelated bytes instead of
table data), so it can't be hardcoded like most of this world's memory
layout. What CAN be hardcoded is each case's anchor (see
core/address_maps/ps2.py's CASE_UNLOCK_BASE_ADDRESSES): the address of
that specific case's own byte in the table, valid to read only while that
case is the one currently loaded (CURRENT_CASE_ADDRESS).

The table IS ordered by case_id (CONFIRMED live for 28 of the 30 cases,
see CASE_UNLOCK_BASE_ADDRESSES's own comment for the 2 exceptions):
1-indexed slot = case_id + 1, slot 1 being a permanently unused/reserved
31st entry. See core/address_maps/ps2.py's CASE_UNLOCK_TABLE_SLOT_TO_CASE
and CASE_NAME_TO_UNLOCK_SLOT.

Since the table is always in the same order regardless of which case
anchors it, any one anchor is enough to derive every other case's address
too, via CASE_UNLOCK_TABLE_OFFSETS (the table's exact, CONFIRMED-live
31-slot layout -- re-derived and cross-checked against 4 independent live
reads anchored on different cases, all matching exactly):

    entry(case_id) = anchor + (CASE_UNLOCK_TABLE_OFFSETS[slot(case_id) - 1]
                                - CASE_UNLOCK_TABLE_OFFSETS[slot(current_case_id) - 1])

_resolve_table() below does exactly this, fresh, every call (i.e. every
tick apply_all()/read_all() run) -- so it always re-derives off whichever
case is CURRENTLY loaded rather than caching a stale absolute address
across a transition.

CaseUnlockInventory resolves the whole 30-entry table off whichever case
is current, then reads/writes it in a single batch_read_int8/
batch_write_int8 call instead of 30 individual ones. Granting a case
UNLOCKED writes 3 (PERMANENTLY_UNLOCKED), not 2 (UNLOCKED) -- CONFIRMED
live, 3 is the value the game itself actually treats as unlocked/playable
on the case-select menu; 2 is written by nothing observed so far and is
kept only as a distinct enum member for read_all() in case it shows up.
Practical effect: once a case is written UNLOCKED it reads back 3, so
apply_all()'s "skip cases already reading PERMANENTLY_UNLOCKED" check
below also works as an idempotent no-op skip for cases it granted itself
last tick, not just the originally-observed natively-3 cases.

resolve_owned_cases() mirrors rules.py's HasPlanet/HasCase item-ownership
checks (case-level Infobot, planet-level Access, and Progressive Planet
tiers) so the in-game case-select menu's lock icons agree with the AP
logic gating those same cases, whichever Infobots granularity a given seed
picked -- see world.py's create_items(), only one of the three tiers is
ever actually in the pool for a given seed, so checking all three here is
just "whichever one exists, if any" rather than needing to know the
option value client-side.

NOT handled here: Character Items gating (see rules.py's HasCharacter) --
that's about which character you can currently play, not whether a case's
entry is locked on the menu, so it's left alone."""
from enum import IntEnum
from typing import TYPE_CHECKING

from ...constants.planets import (
    ALL_CASES,
    CASE_ID_TO_CASE,
    CASE_NAME_TO_INFOBOT,
    CASES_BY_PLANET,
    PLANET_ACCESS_ITEM_NAME,
    PLANET_NAMES,
)
from ...items import PROGRESSIVE_PLANET_ITEM_NAME
from ..address_maps import (
    CASE_NAME_TO_UNLOCK_SLOT,
    CASE_UNLOCK_BASE_ADDRESSES,
    CASE_UNLOCK_TABLE_OFFSETS,
)

if TYPE_CHECKING:
    from ...pypine import Pine


class CaseUnlockState(IntEnum):
    # CONFIRMED live -- 1 was the original placeholder guess and was never
    # actually observed; 0 is the real locked value.
    LOCKED = 0
    # Not what CaseUnlockInventory writes to grant a case -- see
    # PERMANENTLY_UNLOCKED below. Kept as a distinct read-side value in
    # case it ever actually shows up.
    UNLOCKED = 2
    # CONFIRMED live -- this is the value that actually marks a case
    # unlocked/playable on the case-select menu, not UNLOCKED (2). Name
    # kept from when this looked like a separate untracked state some
    # cases natively held; see module docstring / apply_all()'s docstring
    # for why it's used for AP-granted cases too.
    PERMANENTLY_UNLOCKED = 3


def resolve_owned_cases(received_names: list[str], *, character_unlocks: bool = False) -> set[str]:
    """Every case name the player currently has logical access to, derived
    from received item names alone. Generation precollects a randomly chosen
    enabled character's Case File, so no hardcoded starting case is needed here."""
    owned: set[str] = set()

    for case_name, infobot in CASE_NAME_TO_INFOBOT.items():
        if infobot in received_names:
            owned.add(case_name)

    for planet, item in PLANET_ACCESS_ITEM_NAME.items():
        if item in received_names:
            owned.update(case.name for case in CASES_BY_PLANET.get(planet, ()))

    progressive_count = received_names.count(PROGRESSIVE_PLANET_ITEM_NAME)
    if progressive_count:
        for planet in PLANET_NAMES[1:1 + progressive_count]:
            owned.update(case.name for case in CASES_BY_PLANET.get(planet, ()))

    if character_unlocks:
        from ...constants import CHARACTER_ITEM_NAME, PROGRESSIVE_CHARACTER_ITEM_NAME, SACOperatives
        from ...constants.planets import CASES_BY_OPERATIVE
        owned.update(case.name for case in CASES_BY_OPERATIVE[SACOperatives.SPECIAL_MISSIONS])
        for operative, item in CHARACTER_ITEM_NAME.items():
            if item in received_names:
                owned.update(case.name for case in CASES_BY_OPERATIVE[operative])
        for operative, item in PROGRESSIVE_CHARACTER_ITEM_NAME.items():
            owned.update(case.name for case in CASES_BY_OPERATIVE[operative][:received_names.count(item)])
    return owned


class CaseUnlockInventory:
    """Reads/writes every case's locked/unlocked gate in one batch call,
    resolved off whichever case is currently loaded (see module
    docstring). A no-op wherever the current case is unknown or its
    anchor isn't confirmed live yet."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine

    def _resolve_table(self, current_case_id: "int | None") -> dict[str, int]:
        """Every case's live address, re-derived fresh off whichever case
        is CURRENTLY loaded (see module docstring) -- never cached across
        calls, so a case transition since the last call is picked up
        automatically instead of reusing a now-stale table location."""
        current_case = CASE_ID_TO_CASE.get(current_case_id) if current_case_id is not None else None
        if current_case is None:
            return {}
        anchor = CASE_UNLOCK_BASE_ADDRESSES.get(current_case.name, 0)
        if not anchor:
            return {}
        current_slot = CASE_NAME_TO_UNLOCK_SLOT.get(current_case.name)
        if current_slot is None:
            return {}
        current_offset = CASE_UNLOCK_TABLE_OFFSETS[current_slot - 1]
        result = {}
        for case in ALL_CASES:
            slot = CASE_NAME_TO_UNLOCK_SLOT.get(case.name)
            if slot is None:
                continue
            result[case.name] = anchor + (CASE_UNLOCK_TABLE_OFFSETS[slot - 1] - current_offset)
        return result

    def read_all(self, current_case_id: "int | None") -> dict[str, "CaseUnlockState | None"]:
        """Batch-read every case's current locked/unlocked byte."""
        table = self._resolve_table(current_case_id)
        if not table:
            return {}
        names = list(table)
        raw_values = self.pine.batch_read_int8([table[name] for name in names])
        result: dict[str, "CaseUnlockState | None"] = {}
        for name, value in zip(names, raw_values):
            try:
                result[name] = CaseUnlockState(value)
            except ValueError:
                result[name] = None
        return result

    def apply_all(self, owned_case_names: "set[str]", current_case_id: "int | None") -> None:
        """Rebuild every case's unlock gate from AP truth in a single
        batch write -- UNLOCKED for every case in owned_case_names,
        LOCKED otherwise. Written every call (no change-detection skip):
        the game itself can reset a case's byte back to LOCKED on its own
        (e.g. returning to the case-select menu), so re-asserting
        unconditionally every tick is what keeps AP ownership enforced
        rather than just applied once.

        Both native unlocks and previously AP-granted unlocks are reconciled
        with the received inventory. Only skip a byte when it already equals
        the desired state; native state 3 does not imply AP ownership.

        Also skips any slot whose readback ISN'T a recognized
        CaseUnlockState (0/2/3) rather than treating "not 3" as license to
        write -- CONFIRMED live: is_ready flips True the instant
        CURRENT_CASE_ADDRESS itself changes, but the OLD case's table
        memory has been observed already reading garbage (e.g. 192, not a
        valid enum value at all) on the very same tick, i.e. BEFORE
        CURRENT_CASE_ADDRESS has moved off the old case at all -- memory
        teardown for the case being left can start before this address
        updates to reflect it. Blindly writing over a garbage readback
        during that window corrupts whatever's actually there (which by
        the following tick may be a completely different, freshly-loaded
        structure); skipping it here just leaves that slot alone for one
        tick and re-checks 0.1s later (POLL_INTERVAL) once the address
        either settles back into real table data or the transition
        finishes and is_ready gates it off entirely. This is the actual
        mechanism keeping writes off in-flux memory -- is_ready alone
        (case_id-level) doesn't fully cover the transition's leading
        edge."""
        table = self._resolve_table(current_case_id)
        if not table:
            return
        names = list(table)
        addresses = [table[name] for name in names]
        current_values = self.pine.batch_read_int8(addresses)
        recognized = {state.value for state in CaseUnlockState}
        writes = [
            (
                address,
                (CaseUnlockState.PERMANENTLY_UNLOCKED if name in owned_case_names else CaseUnlockState.LOCKED).value,
            )
            for name, address, current in zip(names, addresses, current_values)
            if current in recognized and current != (
                CaseUnlockState.PERMANENTLY_UNLOCKED.value if name in owned_case_names
                else CaseUnlockState.LOCKED.value
            )
        ]
        if writes:
            self.pine.batch_write_int8(writes)

    def force_unlock(self, case_name: str, current_case_id: "int | None") -> bool:
        """Debug/testing helper -- force a single case's gate UNLOCKED
        (writes 3, PERMANENTLY_UNLOCKED -- the real unlocked value, see
        module docstring) without touching any other case's byte. Returns
        False (no-op) if the table can't be resolved right now or
        case_name isn't a known case."""
        table = self._resolve_table(current_case_id)
        address = table.get(case_name)
        if address is None:
            return False
        self.pine.write_int8(address, CaseUnlockState.PERMANENTLY_UNLOCKED.value)
        return True

    def force_lock(self, case_name: str, current_case_id: "int | None") -> bool:
        """Debug/testing helper -- force a single case's gate LOCKED
        without touching any other case's byte. Same caveat as
        force_unlock(): this doesn't grant or revoke AP ownership, so the
        regular per-tick sync flips it back to whatever AP truth says
        (UNLOCKED if actually owned) next tick. Returns False (no-op) if
        the table can't be resolved right now or case_name isn't a known
        case."""
        table = self._resolve_table(current_case_id)
        address = table.get(case_name)
        if address is None:
            return False
        self.pine.write_int8(address, CaseUnlockState.LOCKED.value)
        return True

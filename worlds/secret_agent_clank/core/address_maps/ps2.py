# 2026-09-11 audit: runtime exports now supply GadgetData and pause state.
# Historical case-unlock anchors below overlap mission state fields and MUST
# NOT be applied by the normal client. See docs/address_research.md.
"""Secret Agent Clank PS2 (SCUS-97623) RAM addresses.

Planet/Case model
------------------
Unlike the flat per-planet layout the other RaC worlds use, SAC's world is
Planet -> Case: each planet is split into several Cases (mission chunks),
and it's the *case* id -- not the planet id -- that the transition system
tracks. See constants/planets.py for the Planet/Case tables and
CASE_ID_TO_PLANET for resolving a case back to its parent planet.

Everything below CURRENT_CASE_ADDRESS/FORCE_CASE_ADDRESS is a TODO
placeholder -- fill in through the same live PCSX2/Cheat-Engine process
used for the other RaC worlds' address_maps: find a candidate with Cheat
Engine, convert host address -> PCSX2 PS2 RAM offset, confirm live by
writing a known value and observing the effect in-game, then note it here
as CONFIRMED (see worlds/rac_size_matters_psp/core/address_maps/psp.py for
the style of comment to leave once something's verified).

Per-location addresses (missions, cutscenes, gadgetbot/special/ratchet
challenges, skill points) no longer live here -- each now travels with its
CaseStructure entry in the matching constants/*.py module (see
constants/types.py's CaseStructure), so the name and its address/flag can't
drift out of sync in two separate files. What's left here is genuinely
global (not per-location): case transition, per-case unlock gates, and
plain running counters (bolts, titanium bolts)."""
from dataclasses import dataclass, field

from ...constants.planets import ALL_CASES, CASE_ID_TO_CASE, SACCases

# --- Case transition (CONFIRMED live) --------------------------------------
CURRENT_CASE_ADDRESS = 0x206328  # read: the case currently loaded
FORCE_CASE_ADDRESS    = 0x206324  # write: forces a transition to the given case id

# Value read from CURRENT_CASE_ADDRESS while no case is loaded / a
# transition is in flight. TODO: confirm live -- ported guess from the
# other RaC worlds' idle-value convention (0 == nothing loaded yet).
CASE_IDLE_VALUE: int = 0x00

# --- Titanium bolts (global, not per-case) ----------------------------------

TITANIUM_BOLT_ADDRESS = 0x206C17

# --- Quick select (global, not per-case, CONFIRMED live) --------------------
# The weapon quick-select wheel: 8 slots, 4 bytes (int32) each, back to
# back -- each slot holds the weapon id currently bound to that wheel
# position. Useful for reverse-engineering RATCHET_WEAPONS' real id/name
# mapping (still TODO placeholders, see constants/weapons.py) by watching
# which id appears/disappears as weapons are cycled in-game -- see
# core/quick_select.py.
QUICK_SELECT_ADDRESS = 0x220010
QUICK_SELECT_SLOT_COUNT = 8

# --- Other global (not per-case) addresses (CONFIRMED live) -----------------
CHALLENGE_MODE_ADDRESS = 0x2075D4  # NG+ / NG++ tier
BOLTS_ADDRESS          = 0x2075C8  # bolt currency count
CHEATS_ADDRESS         = 0x206FE0  

# --- Cutscenes (superseded) -------------------------------------------------
# Previously held Boltaire Museum's entry cutscene at 0x206C2D as a
# standalone CONFIRMED-live 0/1 flag, separate from the shared
# 0x206BE0-0x206BF4 bitmask constants/cutscenes.py's CUTSCENES now uses.
# New address/offset data (user-supplied) places that same cutscene at
# 0x206BE0 offset 0x01 instead -- treated as authoritative and superseding
# the old 0x206C2D entry, but flagged here since 0x206C2D was previously
# verified live under a different mechanism; worth double-checking it
# wasn't a real, distinct address before deleting this entirely.
CUTSCENE_ADDRESSES: dict[str, int] = {}

# --- Case unlock gates (per-case anchor into one shared, moving table) -----
# All 30 cases' locked/unlocked bytes live in one table, ordered by
# case_id -- but that table's absolute location in memory moves every time
# the player loads a different case, so it can't be hardcoded like the
# rest of this file. Each entry below is instead that specific case's own
# anchor: the live address of ITS byte in the table, confirmed while that
# case was the one currently loaded. Since the table is always in case_id
# order no matter which case anchors it, any single confirmed anchor is
# enough to derive every other case's address too, by walking
# CASE_UNLOCK_GAPS between them -- see core/case_unlocks.py's
# CaseUnlockInventory, which does that and reads/writes
# constants.types-adjacent CaseUnlockState (0 = locked, 2 = unlocked
# [unconfirmed, nothing observed writes this], 3 = the actual
# unlocked/playable value -- both CONFIRMED live) for the whole table in
# one batch call.
#
# CASE_UNLOCK_BASE_ADDRESSES below is each case's own anchor -- the live
# address of ITS byte in the shared table, confirmed while that case was
# the one currently loaded (see CaseUnlockInventory._resolve_table()).
# Previously guessed via a per-pair CASE_UNLOCK_OFFSET/CASE_UNLOCK_GAP_
# OVERRIDES walk (removed) that only ever worked out for Boltaire Museum's
# own entry -- every OTHER entry it produced actually landed on slot 1 (a
# generic/reserved table slot, id 5503/5504, always state=3) instead of
# that case's own slot, because slot 1 happens to sit close to those
# guessed addresses. Confirmed by: forcing case N via FORCE_CASE_ADDRESS,
# reading CURRENT_CASE_ADDRESS back as N, then locating N's own slot (see
# CASE_UNLOCK_TABLE_SLOT_TO_CASE -- slot = case_id + 1 for every case
# checked) via a live byte-pattern search for that slot's expected id
# (see CASE_UNLOCK_TABLE_OFFSETS below, walked from a known-good id
# sequence), then reading back state=1/id/id+1 at slot_address - 4.
#
# 28 of 30 entries below are CONFIRMED this way, live, one case at a time.
# The 2 exceptions -- COUNTESS_VILLA (case_id 6) and SUCK_AND_JIVE (case_id
# 12) -- could not be force-loaded at all in this pass: writing their
# case_id to FORCE_CASE_ADDRESS was accepted (read back unchanged) but
# CURRENT_CASE_ADDRESS never advanced to them even after 45+ seconds and
# multiple retries/savestate reloads, while every other case_id transitioned
# normally within ~15-30s. Their two entries are instead read out of
# whichever OTHER case's copy of the table happened to be loaded at the
# time (case_id 4's and case_id 11's, respectively) -- every other slot in
# those same reads matched every other confirmed case exactly (see
# CASE_UNLOCK_TABLE_OFFSETS's docstring below), so these two values are
# trusted but not independently self-force-confirmed the way the other 28
# are. Revisit (retry forcing them, ideally after a fresh emulator restart
# rather than a savestate reload) if either ever turns out wrong in
# practice.
CASE_UNLOCK_BASE_ADDRESSES: dict[str, int] = {
    SACCases.BOLTAIRE_MUSEUM:            0x57632C,  # case_id 1  -- CONFIRMED live
    SACCases.BOLTAIRE_GEM_WING:          0x51CC00,  # case_id 2  -- CONFIRMED live
    SACCases.MAX_SECURITY_CELLS:         0x59F9E0,  # case_id 3  -- CONFIRMED live
    SACCases.ROOFTOP_DEATHTRAP:          0x594100,  # case_id 4  -- CONFIRMED live
    SACCases.LARGER_THAN_LIFE:           0x50E360,  # case_id 5  -- CONFIRMED live
    SACCases.COUNTESS_VILLA:             0x5941C0,  # case_id 6  -- NOT self-force-confirmed, see comment above
    SACCases.ASYANICA_ROOFTOPS:          0x565EA0,  # case_id 7  -- CONFIRMED live
    SACCases.GLACIARA_SKI_SLOPES:        0x4FB360,  # case_id 8  -- CONFIRMED live
    SACCases.THE_MESS_HALL:              0x59E0E0,  # case_id 9  -- CONFIRMED live
    SACCases.AZCOTAL_ALLEY:              0x5783A0,  # case_id 10 -- CONFIRMED live
    SACCases.GONDOLA_ASCENT:             0x58F480,  # case_id 11 -- CONFIRMED live
    SACCases.SUCK_AND_JIVE:              0x594580,  # case_id 12 -- NOT self-force-confirmed, see comment above
    SACCases.HIGH_ROLLERS_CASINO:        0x569AC0,  # case_id 13 -- CONFIRMED live
    SACCases.THE_EXERCISE_YARD:          0x5A02A0,  # case_id 14 -- CONFIRMED live
    SACCases.HIGH_STAKES_ROOM:           0x564800,  # case_id 15 -- CONFIRMED live
    SACCases.VENANTONIO_LABS:            0x581560,  # case_id 16 -- CONFIRMED live
    SACCases.VENANTONIO_CANALS:          0x5059A0,  # case_id 17 -- CONFIRMED live
    SACCases.MADAM_BUTTERQWARK:          0x51F6E0,  # case_id 18 -- CONFIRMED live
    SACCases.GALACTIC_BOLT_RESERVE:      0x582C80,  # case_id 19 -- CONFIRMED live
    SACCases.INSIDE_THE_A_EYE:           0x512360,  # case_id 20 -- CONFIRMED live
    SACCases.THE_SHOWERS:                0x598E20,  # case_id 21 -- CONFIRMED live
    SACCases.SPACESHIP_GRAVEYARD:        0x587AE0,  # case_id 22 -- CONFIRMED live
    SACCases.SAINT_QWARK:                0x5181C0,  # case_id 23 -- CONFIRMED live
    SACCases.THE_QUASAR_FIELDS:          0x52D220,  # case_id 24 -- CONFIRMED live
    SACCases.PRISON_BREAKOUT:            0x5A5600,  # case_id 25 -- CONFIRMED live
    SACCases.DAMS_EDGE_HYDRANO:          0x50F5C0,  # case_id 26 -- CONFIRMED live
    SACCases.A_FICTION_FULL_OF_DOLLARS:  0x5174E0,  # case_id 27 -- CONFIRMED live
    SACCases.BULKHEAD_LOCK:              0x510BC0,  # case_id 28 -- CONFIRMED live
    SACCases.UNDERWATER_BUNKER:          0x589DE0,  # case_id 29 -- CONFIRMED live
    SACCases.KLUNKS_LAIR:                0x568EE0,  # case_id 30 -- CONFIRMED live
}

# --- Case-unlock table, exact layout ----------------------------------------
# CONFIRMED live: this is the real 31-slot case-unlock table itself, not a
# separate per-case struct -- offset 0x000 here IS the same
# locked/unlocked byte CASE_UNLOCK_BASE_ADDRESSES/CaseUnlockInventory
# already tracks for whichever case anchors it (it lines up exactly with
# CASE_UNLOCK_BASE_ADDRESSES's Boltaire Museum entry, 0x57632C -- slot 2
# below). Each slot's byte is 0 (LOCKED) or 3 (UNLOCKED), same
# CaseUnlockState semantics as case_unlocks.py.
#
# This exact list of 31 relative offsets is stable regardless of which
# case is currently anchoring the table -- re-derived and cross-checked
# against 4 independent live table reads (anchored on case_ids 11, 13, 14,
# and originally Boltaire Museum): all 31 slot ids matched exactly every
# time. What DOES move is the table's absolute location in memory -- it
# relocates on every single case transition (confirmed: reading the same
# absolute address again after transitioning to a different case, with no
# intervening savestate reload, returned code/unrelated bytes instead of
# table data). CASE_UNLOCK_BASE_ADDRESSES's anchor for whichever case is
# CURRENTLY loaded is therefore the only fixed reference point at any
# given moment -- see CaseUnlockInventory._resolve_table(), which derives
# every other case's address from these offsets relative to that one
# anchor, fresh, every tick (so it self-corrects across transitions
# instead of caching a stale absolute address).
CASE_UNLOCK_TABLE_OFFSETS: tuple[int, ...] = (
    -0xC0, 0x000, 0x060, 0x140, 0x260, 0x2C0, 0x320, 0x380, 0x440, 0x540,
    0x600, 0x660, 0x6E0, 0x7A0, 0x800, 0x860, 0x8C0, 0x980, 0xA40, 0xAE0,
    0xBC0, 0xC80, 0xD40, 0xDA0, 0xE00, 0xE60, 0xF20, 0x1040, 0x10A0, 0x11C0,
    0x1220,
)

# 1-indexed slot (position in CASE_UNLOCK_TABLE_OFFSETS above, in order) ->
# SACCases name. CONFIRMED live: slot = case_id + 1 for every one of the 30
# cases (slot 1 is a permanently unused/reserved 31st entry -- id
# 5503/5504, state always 3 -- never a real case). Verified by forcing
# each case_id (except 6 and 12, see CASE_UNLOCK_BASE_ADDRESSES's comment)
# and finding its own slot at exactly this position, with zero exceptions
# across all 5 SACOperatives types.
CASE_UNLOCK_TABLE_SLOT_TO_CASE: dict[int, str] = {
    case.case_id + 1: case.name for case in ALL_CASES
}
# Reverse of the above, for resolving "this case's own slot index" without
# a linear scan (see CaseUnlockInventory._resolve_table() and
# CaseStructInventory._resolve_anchor()).
CASE_NAME_TO_UNLOCK_SLOT: dict[str, int] = {
    name: slot for slot, name in CASE_UNLOCK_TABLE_SLOT_TO_CASE.items()
}

# --- Gadgetbot Challenges (per-case unlock gate) ----------------------------
# All cases' Gadgetbot Challenges share ONE long, irregularly-packed struct
# -- see constants/gadgetbot_challenges.py's GADGETBOT_CHALLENGES for the
# per-challenge completed-flag addresses. This dict is just the separate
# per-case unlock gate (not itself an AP location, just a prerequisite --
# exact semantics unconfirmed, read 0/1 so far).
GADGETBOT_UNLOCK_ADDRESSES: dict[str, int] = {
    SACCases.INSIDE_THE_A_EYE: 0x206C77,
    SACCases.BULKHEAD_LOCK:    0x206C79,
}

# --- Special Challenges (per-case unlock gate) ------------------------------
# Same deal as GADGETBOT_UNLOCK_ADDRESSES above, for Special Missions-
# operative cases -- see constants/special_challenges.py's
# SPECIAL_CHALLENGES for the per-challenge completed-flag addresses. Lands
# in the same address region as the Gadgetbot Challenges' unlock bytes
# (0x206C99 is +0x1F past Bulkhead Lock's unlock at 0x206C79).
SPECIAL_CHALLENGE_UNLOCK_ADDRESSES: dict[str, int] = {
    SACCases.VENANTONIO_CANALS:   0x206C99,
    SACCases.DAMS_EDGE_HYDRANO:   0x206C9A,
    SACCases.GLACIARA_SKI_SLOPES: 0x206C98,
}


@dataclass(frozen=True)
class CaseAddresses:
    """Every address that's specific to one Case, all TODO/unconfirmed
    unless noted.

    weapon_array is the base of THIS case's WeaponData struct array --
    Ratchet's full 40-slot weapon/tool/wrench-ability table (see
    core/weapons.py's WEAPON_ORDER/WEAPON_STRUCT_SIZE for the layout,
    confirmed via Ghidra/PINE). It's a single base address rather than a
    flattened per-name dict, the same way core/address_maps/psp.py's
    WEAPON_ARRAY_BASE_BY_PLANET feeds WeaponInventory on the other RaC
    worlds -- core/weapons.py's build_weapons() derives every named slot's
    address as weapon_array + slot_index * WEAPON_STRUCT_SIZE.
    NOT yet mapped to a case_id here: the two array bases confirmed so far
    (via Ghidra decompilation of two different savestates) haven't been
    tied back to a specific case_id yet, so every entry below still leaves
    weapon_array as None until that mapping is done, case by case, the same
    live-PINE-plus-Ghidra process used to find the struct layout itself.

    clank_gadget_addrs is a name -> "unlocked flag address" map for Clank's
    spy gadgets (see constants/clank_gadgets.py) -- a separate, still
    entirely unmapped system from Ratchet's WeaponData table above. Qwark
    has no item inventory -- see core/planets.py.
    """
    case_id: int
    ratchet_state:  int | None = None
    ratchet_health: int | None = None
    clank_state:    int | None = None
    clank_health:   int | None = None
    qwark_state:    int | None = None
    qwark_health:   int | None = None
    menu:                     int | None = None
    vendor_items:             int | None = None
    mission:                  int | None = None
    controller_pause_select:  int | None = None
    weapon_array:         int | None = None
    clank_gadget_addrs:   dict[str, int] = field(default_factory=dict)


# --- Weapon array bases (per-case, CONFIRMED live as each case is visited --
# see core/weapons.py's WEAPON_ORDER/WEAPON_STRUCT_SIZE for the struct this
# is the base of). Found via the same Ghidra/PINE process used to derive the
# struct layout itself: savestate -> extract EE RAM -> byte-search for a
# known weapon name string (e.g. "blaster") -> byte-search for a pointer to
# that string's address (lands on WeaponData[2], the first named slot) ->
# subtract 2 * WEAPON_STRUCT_SIZE to get slot 0's (the array's) base --
# then live-PINE-confirmed by reading a plausible ammo/owned pair off it.
WEAPON_ARRAY_BASE_BY_CASE: dict[int, int] = {
    1: 0x0057AAF8,  # Boltaire Museum -- CONFIRMED live (savestate slot 10; slot0 name=0/cat=0,
                     # slot2 "blaster" ammo=80/owned=0, matching the struct layout exactly)
    2: 0x00521378,  # Boltaire Gem Wing -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 2; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0). Same
                     # numeric base as the very first eeMemory.bin dump analyzed in Ghidra
                     # ("After Mission One.bin") -- unconfirmed whether that dump was actually
                     # captured on this case or the two just landed on the same DLL-buffer slot.
    4: 0x00598678,  # Rooftop Deathtrap -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 4 across three separate savestates, including one deliberately
                     # navigated to and confirmed as "Rooftop Deathtrap" in-game -- resolves an
                     # earlier mix-up where this same case_id/address was reached while the user
                     # believed they were on Asyanica Rooftops [case_id 7] instead; slot0 name=0/
                     # cat=0, slot2 "blaster" ammo=80/owned=0).
    10: 0x0057C578,  # Azcotal Alley -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 10; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    11: 0x005935F8,  # Gondola Ascent -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 11; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    12: 0x005935F8,  # Suck and Jive -- ALIASED to Gondola Ascent's base, not a separate discovery.
                      # Investigated a suspected case_id collision: CURRENT_CASE_ADDRESS reads 11
                      # (not 12) while on Suck and Jive, and weapon_array cross-validates to this
                      # same 0x5935F8 base every time (checked across two independent savestate/
                      # extract captures). Searched for a separate "current character" address to
                      # disambiguate (per user request, via Ghidra's SN Systems debug-symbol table
                      # anchored off "WEAPON_") -- found no character/player-switch symbols nearby.
                      # Then did a direct live-memory diff instead: read the full 0x300-byte block
                      # around CURRENT_CASE_ADDRESS (0x206200-0x206500) once while confirmed on
                      # Suck and Jive and again while confirmed on Gondola Ascent (user reported a
                      # genuine loading screen between the two) -- the two reads were BYTE-IDENTICAL,
                      # including unrelated fields (e.g. a heap pointer at 0x206370) that would be
                      # expected to differ across a true case reload. Conclusion: Suck and Jive does
                      # not get its own case-data blob at all -- it reuses Gondola Ascent's case_id
                      # (11) and weapon_array wholesale at the engine level, despite showing its own
                      # loading screen and being modeled as a separate Case/operative in constants/
                      # planets.py. No separate character-tracking address exists to find because
                      # there is nothing distinguishing the two states in memory. Aliasing this
                      # table entry to case 11's base is therefore correct, not a workaround.
    18: 0x00523478,  # Madam Butterqwark -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 18; slot0 name=0/cat=0, slot1 cat=2/no name, slot2 "blaster"
                      # ammo=80/owned=0; cross-validated against 6 other weapon names' slots
                      # [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion] all resolving
                      # to this same table_base).
    23: 0x0051BBF8,  # Saint Qwark -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 23; slot0 name=0/cat=0, slot1 cat=2/no name, slot2 "blaster"
                      # ammo=80/owned=0; cross-validated against 6 other weapon names' slots
                      # [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion] all resolving
                      # to this same table_base).
    27: 0x0051AC78,  # A Fiction Full Of Dollars -- CONFIRMED live (savestate slot 10;
                      # CURRENT_CASE_ADDRESS read back as 27; slot0 name=0/cat=0, slot1 cat=2/no
                      # name, slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other
                      # weapon names' slots [shardgun, walloper, ryno, hypnowatch, jetboots,
                      # kicksplosion] all resolving to this same table_base).
    8: 0x004FF6F8,  # Glaciara Ski Slopes -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 8, no mismatch this time; slot0 name=0/cat=0, slot1 cat=2/no
                     # name, slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other
                     # weapon names' slots [shardgun, walloper, ryno, hypnowatch, jetboots,
                     # kicksplosion] all resolving to this same table_base).
    15: 0x00568778,  # High Stakes Room -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 15, no mismatch; slot0 name=0/cat=0, slot1 cat=2/no name,
                      # slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other weapon
                      # names' slots [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion]
                      # all resolving to this same table_base).
    17: 0x005097F8,  # Venantonio Canals -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 17, no mismatch; slot0 name=0/cat=0, slot1 cat=2/no name,
                      # slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other weapon
                      # names' slots [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion]
                      # all resolving to this same table_base).
    24: 0x00530BF8,  # The Quasar Fields -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 24, no mismatch; slot0 name=0/cat=0, slot1 cat=2/no name,
                      # slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other weapon
                      # names' slots [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion]
                      # all resolving to this same table_base).
    26: 0x00512E78,  # Dam's Edge, Hydrano -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 26, no mismatch; slot0 name=0/cat=0, slot1 cat=2/no name,
                      # slot2 "blaster" ammo=80/owned=0; cross-validated against 6 other weapon
                      # names' slots [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion]
                      # all resolving to this same table_base).
    7: 0x0056A2F8,  # Asyanica Rooftops -- CONFIRMED via direct FORCE_CASE_ADDRESS write (wrote 7 to
                     # 0x206324, CURRENT_CASE_ADDRESS then read back as 7, FORCE_CASE_ADDRESS reset
                     # to its idle sentinel -1). Resolves a repeated menu mixup: every prior attempt
                     # to reach this case by clicking "Asyanica Rooftops" in the case-select menu
                     # actually landed on case_id 4 (Rooftop Deathtrap) instead, and a separate
                     # attempt believed to be "Countess's Villa" also turned out to read this exact
                     # same table_base (0x56A2F8) -- both were misclicks, not an engine-level
                     # shared-case quirk (proven by forcing case_id 7 directly and getting genuinely
                     # distinct data from case 4). slot0 name=0/cat=0, slot1 cat=2/no name, slot2
                     # "blaster" ammo=80/owned=0; cross-validated against 6 other weapon names'
                     # slots [shardgun, walloper, ryno, hypnowatch, jetboots, kicksplosion] all
                     # resolving to this same table_base).
    13: 0x0056DAF8,  # High-Rollers Casino -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 13; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    16: 0x00585478,  # Venantonio Labs -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 16; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    19: 0x00586978,  # Galactic Bolt Reserve -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 19; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    29: 0x0058D3F8,  # Underwater Bunker -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 29; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    22: 0x0058B578,  # Spaceship Graveyard -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 22; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    30: 0x0056C4F8,  # Klunk's Lair -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 30; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    3: 0x005A4078,  # Max-Security Cells -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 3; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    9: 0x005A2378,  # The Mess Hall -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 9; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    14: 0x005A4278,  # The Exercise Yard -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 14; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    21: 0x0059C978,  # The Showers -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 21; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    25: 0x005A8F78,  # Prison Breakout! -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 25; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    20: 0x00515F78,  # Inside the A-Eye -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 20; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    28: 0x005142F8,  # Bulkhead Lock -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                      # read back as 28; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
    5: 0x00512878,  # Larger Than Life -- CONFIRMED live (savestate slot 10; CURRENT_CASE_ADDRESS
                     # read back as 5; slot0 name=0/cat=0, slot2 "blaster" ammo=80/owned=0).
                     # This dump had a second, coincidental "blaster\0" byte sequence earlier in
                     # memory unrelated to the WeaponData table (misaligned, no pointer to it) --
                     # cross-validated via 6 other weapon-name slots (shardgun/walloper/ryno/
                     # hypershot/jetboots/bolttransfer) all agreeing on this same table base.
}

# --- Vendor screen (case-relative offset from weapon_array, mirrors how
# WEAPON_STRUCT_SIZE generalizes weapon-slot offsets across every case) -----
# The vendor screen (SCRNVENDOR_Init/Update/Render/Exit/ProcessPurchase --
# located via Ghidra string-scan + backward-pointer symbol lookup on
# forced_ratchet_case3.bin, the SN Systems bulk symbol table having proven
# unreliable -- see docs/) keeps its own state INSIDE the same per-case
# streamed module as the WeaponData table, NOT in the persistent/global
# low-memory region bolts/quick-select/challenge-mode live in (those are
# all < 0x21_0000; these are in the same 0x4F_xxxx-0x5A_xxxx range as
# WEAPON_ARRAY_BASE_BY_CASE). Two fixed offsets from that case's
# weapon_array, CONFIRMED structurally live on two INDEPENDENT cases (case
# 3, via the Ghidra snapshot; case 4, via a live PINE read while that case
# was actually loaded):
#   - weapon_array + VENDOR_SCREEN_STATE_OFFSET: SCRNVENDOR_Update's own
#     DAT_005af4e8 field (as named in the case-3 snapshot) -- reset to 0 by
#     SCRNVENDOR_Init, compared against small values (0/1/2) in
#     SCRNVENDOR_Update's decompiled body. Read live on case 4 (idle, no
#     vendor open) as 0, matching Init's reset value.
#   - weapon_array + VENDOR_SLOT_ARRAY_OFFSET: the vendor's 6-slot item
#     array header (SCRNVENDOR_Init loops FUN_003c2d00(i) for i in 0..5,
#     each call bounds-checked against this header's count field via
#     FUN_003bf050). Its count field (+4) read back as exactly 6 on BOTH
#     cases, and its first field (a self-relative pointer, base-0x20)
#     matched exactly on both: case 3 -> struct at 0x5afa80, first field
#     0x5afa60; case 4 (address only ever derived from this offset, never
#     hand-picked) -> struct at 0x5a4080, first field 0x5a4060. A
#     byte-for-byte structural match at a purely *derived* offset on a
#     completely independent case is the strongest evidence available
#     (short of an actual open-vendor capture) that this offset pair
#     generalizes to every case exactly like WEAPON_STRUCT_SIZE does.
#
# UPDATE, live-tested with a real open vendor screen (user stood at an
# actual in-game vendor while this was polled): VENDOR_SCREEN_STATE_OFFSET
# below is DISPROVEN as an "is open" signal -- it read 0 both before AND
# during a confirmed-open vendor screen, and the wider region around it
# (including VENDOR_SLOT_ARRAY_OFFSET's whole table) was BYTE-IDENTICAL
# open vs. closed. Root cause, found by decompiling SCRNVENDOR_Update
# itself: DAT_005af4e8 (this offset's target) is read/written *inside*
# SCRNVENDOR_Update's own body, which the screen-manager only calls while
# SCRNVENDOR is already the active screen -- so nothing inside it can ever
# tell you "closed" from the outside; it's a sub-state for in-screen button
# handling (its 0/1/2 values gate calls into FUN_0050f9f0/FUN_0034e918/
# FUN_003c2118, most likely "close"/"switch tab" actions), not an open/
# closed toggle. VENDOR_SLOT_ARRAY_OFFSET's 6-entry table is similarly NOT
# vendor item data -- decompiling its populator (FUN_003c2d00, called with
# 0..5 from SCRNVENDOR_Init) shows it's a generic 6-icon HUD status strip
# (button/analog-stick state icons read off a controller/player struct via
# PTR_DAT_005a5630) that many different screens refresh on Init, not
# something specific to a vendor's items -- its "6" was a coincidental
# match to SCRNVENDOR_Init's own unrelated 6-slot loop, not confirmation.
#
# The real "current active screen" signal almost certainly exists as a
# global of the game's own `ePAUSEMODE_SCREENS` enum (see
# PAUSEMODE_GetCurrentPauseScreen/PAUSEMODE_RequestScreen/
# PAUSEMODE_PushAndRequestPauseScreen in the binary's debug string table,
# plus real vendor-purchase UI strings "BUY AMMO"/"BUY GADGET"/"BUY MAX
# AMMO"/"ENTRVENDOR" confirming SCRNVENDOR genuinely is the buy screen) --
# but resolving PAUSEMODE_GetCurrentPauseScreen's real address via the
# string-scan+backward-pointer technique gave a 1-byte non-function stub
# (a bad match), and PAUSEMODE_RequestScreen's resolved the same way
# turned out to be a generic templated stack-pop
# (Pop__t5Stack2Z18ePAUSEMODE_SCREENSUi8), not the real dispatcher -- this
# technique, reliable for the SCRNVENDOR_* cluster earlier, is clearly not
# 100% reliable for every symbol-table entry. Left as TODO: find
# PAUSEMODE's real current-screen global (by decompiling whichever
# function actually switches on ePAUSEMODE_SCREENS to call each SCRNxxx_
# Update, or by a live diff of a *narrow, targeted* address once the right
# region is known) and, separately, find the vendor's real per-slot
# item/price data (still unlocated -- the 232-byte "slot" structs found
# case-relative to weapon_array are NOT it, see above).
#
# VENDOR_SCREEN_STATE_OFFSET/VENDOR_SLOT_ARRAY_OFFSET are left below,
# unused by CaseAddresses.menu now, as a documented dead end so this isn't
# re-derived from scratch next time.
VENDOR_SCREEN_STATE_OFFSET = 0xB470  # DISPROVEN as an open/closed signal -- see above
VENDOR_SLOT_ARRAY_OFFSET   = 0xB9C8  # NOT vendor item data -- a generic 6-icon HUD status strip, see above
VENDOR_SLOT_COUNT          = 6  # SCRNVENDOR_Init's fixed slot loop (i in 0..5) -- coincidental match, not confirmation

# --- Vendor ITEM list (CONFIRMED live -- this is the real one, found by
# tracing the actual call graph instead of guessing addresses near
# weapon_array, per user direction, after VENDOR_SCREEN_STATE_OFFSET/
# VENDOR_SLOT_ARRAY_OFFSET above both proved to be dead ends) -------------
# The vendor's item list is populated by FUN_003d2b28 (called from the
# case-8/0x10 pause-screen Init, FUN_003d2958), which loops item ids
# 0..0x27 (the same 0-39 range as WEAPON_ORDER) and inserts qualifying ones
# via FUN_003db1c8 into a fixed-size backing array at DAT_005b7ff0 (case-3
# Ghidra snapshot address). That backing array sits at a FIXED OFFSET from
# weapon_array -- 0x5b7ff0 - (0x5afa80 - VENDOR_SLOT_ARRAY_OFFSET) [case 3's
# own weapon_array, back-derived the same way case 4's was cross-checked
# above] = 0x13F38 -- so it generalizes across cases exactly like
# weapon_array and VENDOR_SLOT_ARRAY_OFFSET do.
#
# LIVE-CONFIRMED on case 4 with the vendor genuinely open (weapon_array +
# 0x13F38 = 0x5AC5B0): 8 populated 0x1C(28)-byte nodes followed by zero
# padding. Node layout (int32 fields, offsets from each node's start):
#   +0x00  1 for every populated node (0 = unpopulated/padding -- stop here)
#   +0x04  small icon/category id (seen: 50/51 -- NOT a weapon id)
#   +0x08  unused/0 in every node seen so far
#   +0x0C  node type -- 3 was the only value observed live (weapon-mod
#          offer, matching FUN_003d2b28's node_type=3 call for
#          SCRNVENDOR_IsWeaponMod items; type 0/2/4 exist in the source per
#          that function's other call sites -- weapon/ammo-bundle/
#          titan-weapon -- but weren't seen live since only mods were on
#          offer during the capture)
#   +0x10  WEAPON_ORDER slot id (0-39) -- confirmed against real weapon
#          names: live capture showed [2, 2, 4, 4, 5, 7, 9, 9] = blaster,
#          blaster, beemineglove, beemineglove, shockrocket, plasmawhip,
#          minelauncher, minelauncher (slot 9 = minelauncher matches the
#          weapon whose mod purchase was independently confirmed via the
#          WeaponData-table byte diff -- see core/weapons.py's
#          _OFFSET_MOD_SLOTS)
#   +0x14  mod id in a separate, larger, game-wide mod catalog (NOT the 0-2
#          per-weapon mod-slot index from _OFFSET_MOD_SLOTS) -- live values
#          seen: [1, 2, 7, 8, 10, 17, 23, 23]
#   +0x18  unused/0 in every node seen so far
# No confirmed "count" field yet (the list-widget's own control struct,
# DAT_006fd178/DAT_0067d78c in the case-3 snapshot, did NOT respond to the
# same weapon_array-relative shift that correctly located the backing
# array above -- reads as all zero live even with the vendor open, so it
# likely belongs to a different, not-yet-understood base). Read the node
# array directly and stop at the first inactive (+0x00 == 0) node instead.
VENDOR_ITEM_ARRAY_OFFSET = 0x13F38
VENDOR_ITEM_STRIDE       = 0x1C   # bytes per node
VENDOR_ITEM_MAX_COUNT    = 32     # generous cap -- read until an inactive node or this many
_ITEM_OFFSET_ACTIVE    = 0x00
_ITEM_OFFSET_ICON      = 0x04
_ITEM_OFFSET_NODE_TYPE = 0x0C
_ITEM_OFFSET_WEAPON_ID = 0x10
_ITEM_OFFSET_MOD_ID    = 0x14

# One entry per known case id -- every field but weapon_array is still
# TODO/None; fill them in as addresses are found, case by case. menu is
# NOT derived from weapon_array anymore -- VENDOR_SCREEN_STATE_OFFSET above
# was live-tested against a real open vendor screen and disproven, so
# leaving menu=None here (honestly unmapped) beats shipping an address
# already known to read 0 whether the vendor is open or closed.
CASE_ADDRESSES: dict[int, CaseAddresses] = {
    case_id: CaseAddresses(
        case_id=case_id,
        weapon_array=WEAPON_ARRAY_BASE_BY_CASE.get(case_id),
        vendor_items=(
            WEAPON_ARRAY_BASE_BY_CASE[case_id] + VENDOR_ITEM_ARRAY_OFFSET
            if case_id in WEAPON_ARRAY_BASE_BY_CASE else None
        ),
    )
    for case_id in CASE_ID_TO_CASE
}

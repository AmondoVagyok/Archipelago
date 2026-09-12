"""SAC's world has two independent axes over its 30 cases:

  - Planet: which of the 10 planets a case takes place on. Cases are
    grouped by CURRENT_CASE_ADDRESS/FORCE_CASE_ADDRESS at the memory
    level (see core/address_maps/ps2.py) -- best-effort guess from
    name/theme clues, NOT confirmed (see LOW CONFIDENCE comments below).

  - Operative: which of the game's own "Operatives" menu groups a case is
    filed under (Ratchet / Clank / Gadgetbots / Qwark / Special Missions)
    -- CONFIRMED real for 22/30 cases from user-supplied screenshots of
    that exact menu (see constants/operatives.py); the remaining 8 are
    inferred from skill point flavor text (e.g. "Qwarkography Ch. 3" ->
    Qwark, Holo-Monocle/Blackout Pen stealth -> Clank) and marked LOW
    CONFIDENCE the same way.

Every Case carries both, independently -- see the Case dataclass.
case_id values are NOT real memory values yet -- they're just the case's
position (1-30) in the flat Case Files list as originally given, used as a
stable placeholder key until each case's real CURRENT_CASE_ADDRESS value
is confirmed live and swapped in here. case_id 1 (Boltaire Museum) is the
first one CONFIRMED live via /force_case 1 -- see the per-case comments
below as more are verified the same way.
"""
from dataclasses import dataclass

from .operatives import SACOperatives


@dataclass(frozen=True)
class SACPlanets:
    """String constants for each planet."""

    BOLTAIRE_MUSEUM = "Boltaire Museum"
    PRISON_PLANET = "Prison Planet"
    ASYANICA = "Asyanica"
    GLACIARA = "Glaciara"
    RIONOSIS = "Rionosis"
    CASINO = "Le Paradis Des Tricheurs Casino"
    VENANTONIO = "Venantonio"
    FORT_SPROCKET = "Fort Sprocket"
    SPACESHIP_GRAVEYARD = "Spaceship Graveyard"
    HYDRANO = "Hydrano"


@dataclass(frozen=True)
class SACCases:
    """String constants for each case."""

    BOLTAIRE_MUSEUM = "Boltaire Museum"
    BOLTAIRE_GEM_WING = "Boltaire Gem Wing"
    MAX_SECURITY_CELLS = "Max-Security Cells"
    ROOFTOP_DEATHTRAP = "Rooftop Deathtrap"
    ASYANICA_ROOFTOPS = "Asyanica Rooftops"
    LARGER_THAN_LIFE = "Larger Than Life"
    COUNTESS_VILLA = "Countess's Villa"
    GLACIARA_SKI_SLOPES = "Glaciara, Ski Slopes"
    THE_MESS_HALL = "The Mess Hall"
    AZCOTAL_ALLEY = "Azcotal Alley"
    GONDOLA_ASCENT = "Gondola Ascent"
    SUCK_AND_JIVE = "Suck and Jive"
    HIGH_ROLLERS_CASINO = "High-Rollers Casino"
    THE_EXERCISE_YARD = "The Exercise Yard"
    HIGH_STAKES_ROOM = "High Stakes Room"
    VENANTONIO_LABS = "Venantonio Labs"
    VENANTONIO_CANALS = "Venantonio Canals"
    MADAM_BUTTERQWARK = "Madam Butterqwark"
    GALACTIC_BOLT_RESERVE = "Galactic Bolt Reserve"
    INSIDE_THE_A_EYE = "Inside the A-Eye"
    THE_SHOWERS = "The Showers"
    SPACESHIP_GRAVEYARD = "Spaceship Graveyard"
    SAINT_QWARK = "Saint Qwark"
    THE_QUASAR_FIELDS = "The Quasar Fields"
    PRISON_BREAKOUT = "Prison Breakout!"
    DAMS_EDGE_HYDRANO = "Dam's Edge, Hydrano"
    A_FICTION_FULL_OF_DOLLARS = "A Fiction Full Of Dollars"
    BULKHEAD_LOCK = "Bulkhead Lock"
    UNDERWATER_BUNKER = "Underwater Bunker"
    KLUNKS_LAIR = "Klunk's Lair"
    HIGH_TREEHOUSE = "High Impact Treehouse"


@dataclass(frozen=True)
class Case:
    name: str
    case_id: int
    planet: str       # SACPlanets constant
    operative: str    # SACOperatives constant
    # Separate numbering scheme from case_id -- case_id is
    # CURRENT_CASE_ADDRESS/FORCE_CASE_ADDRESS's id (what /force_case
    # verifies); menu_id is this case's position in the case-select
    # menu's own list (what /force_menu, /unlock_case, /case_states
    # anchor off, via CASE_UNLOCK_BASE_ADDRESSES). CONFIRMED live these
    # are NOT always the same value for the same case (e.g. Larger Than
    # Life is case_id 5 but menu_id 8) -- don't assume one from the
    # other. None until individually verified.
    menu_id: "int | None" = None


# Order matches the original Case Files list (case_id 1-30). planet is
# best-guess (see module docstring); operative is CONFIRMED for the first
# 22 (from the user's Operatives-menu screenshots) and LOW CONFIDENCE for
# the remaining 8, inferred from skill point flavor text -- see the
# per-case comments.
ALL_CASES: tuple[Case, ...] = (
    # case_id CONFIRMED live via /force_case 1
    Case(SACCases.BOLTAIRE_MUSEUM, 1, SACPlanets.BOLTAIRE_MUSEUM, SACOperatives.CLANK),
    # case_id CONFIRMED live via /force_case 2
    Case(SACCases.BOLTAIRE_GEM_WING, 2, SACPlanets.BOLTAIRE_MUSEUM, SACOperatives.SPECIAL_MISSIONS),
    # case_id CONFIRMED live via /force_case 3
    Case(SACCases.MAX_SECURITY_CELLS, 3, SACPlanets.PRISON_PLANET, SACOperatives.RATCHET),
    # case_id CONFIRMED live via /force_case 4; planet still LOW CONFIDENCE — escape sequence, guessed prison rather than Asyanica
    Case(SACCases.ROOFTOP_DEATHTRAP, 4, SACPlanets.ASYANICA, SACOperatives.GADGETBOTS),
    # case_id CONFIRMED live via /force_case 5 -- was previously (wrongly) 6, swapped with Asyanica Rooftops below
    # menu_id CONFIRMED live -- 8, from the case-select menu list (a
    # separate numbering scheme from case_id, see Case dataclass)
    Case(SACCases.LARGER_THAN_LIFE, 5, SACPlanets.ASYANICA, SACOperatives.QWARK, menu_id=8),
    # case_id not yet re-verified -- was previously (wrongly) 5, then (wrongly) 6
    Case(SACCases.COUNTESS_VILLA, 6, SACPlanets.GLACIARA, SACOperatives.SPECIAL_MISSIONS),
    # case_id CONFIRMED live via /force_case 7 -- was previously (wrongly) 6, swapped with Countess's Villa above
    Case(SACCases.ASYANICA_ROOFTOPS, 7, SACPlanets.ASYANICA, SACOperatives.CLANK),
    # menu_id CONFIRMED live -- 10, from the case-select menu list (see Case dataclass)
    Case(SACCases.GLACIARA_SKI_SLOPES, 8, SACPlanets.GLACIARA, SACOperatives.SPECIAL_MISSIONS, menu_id=10),
    # menu_id CONFIRMED live -- 12, from the case-select menu list (see Case dataclass)
    Case(SACCases.THE_MESS_HALL, 9, SACPlanets.PRISON_PLANET, SACOperatives.RATCHET, menu_id=12),
    # planet LOW CONFIDENCE
    Case(SACCases.AZCOTAL_ALLEY, 10, SACPlanets.GLACIARA, SACOperatives.CLANK),
    # planet LOW CONFIDENCE — assumed ski-lift, not Venantonio's canal gondolas
    Case(SACCases.GONDOLA_ASCENT, 11, SACPlanets.GLACIARA, SACOperatives.CLANK),
    # planet LOW CONFIDENCE — only leftover planet, no name clue tying it here
    Case(SACCases.SUCK_AND_JIVE, 12, SACPlanets.RIONOSIS, SACOperatives.QWARK),
    Case(SACCases.HIGH_ROLLERS_CASINO, 13, SACPlanets.CASINO, SACOperatives.CLANK),
    Case(SACCases.THE_EXERCISE_YARD, 14, SACPlanets.PRISON_PLANET, SACOperatives.RATCHET),
    Case(SACCases.HIGH_STAKES_ROOM, 15, SACPlanets.CASINO, SACOperatives.SPECIAL_MISSIONS),
    Case(SACCases.VENANTONIO_LABS, 16, SACPlanets.VENANTONIO, SACOperatives.CLANK),
    Case(SACCases.VENANTONIO_CANALS, 17, SACPlanets.VENANTONIO, SACOperatives.SPECIAL_MISSIONS),
    # planet LOW CONFIDENCE; operative LOW CONFIDENCE — inferred from "Qwarkography Ch. 3" flavor text
    Case(SACCases.MADAM_BUTTERQWARK, 18, SACPlanets.VENANTONIO, SACOperatives.QWARK),
    # planet LOW CONFIDENCE; operative LOW CONFIDENCE — inferred from disguise/stealth flavor text
    Case(SACCases.GALACTIC_BOLT_RESERVE, 19, SACPlanets.VENANTONIO, SACOperatives.CLANK),
    # planet LOW CONFIDENCE
    Case(SACCases.INSIDE_THE_A_EYE, 20, SACPlanets.FORT_SPROCKET, SACOperatives.GADGETBOTS),
    # planet LOW CONFIDENCE
    Case(SACCases.THE_SHOWERS, 21, SACPlanets.PRISON_PLANET, SACOperatives.RATCHET),
    # operative LOW CONFIDENCE — inferred from Holo-Monocle stealth flavor text
    Case(SACCases.SPACESHIP_GRAVEYARD, 22, SACPlanets.SPACESHIP_GRAVEYARD, SACOperatives.CLANK),
    # operative LOW CONFIDENCE — inferred from "Qwarkography Ch. 4" flavor text (name itself is a strong clue too)
    Case(SACCases.SAINT_QWARK, 23, SACPlanets.SPACESHIP_GRAVEYARD, SACOperatives.QWARK),
    # operative LOW CONFIDENCE — inferred from space-combat/vehicle flavor text
    Case(SACCases.THE_QUASAR_FIELDS, 24, SACPlanets.SPACESHIP_GRAVEYARD, SACOperatives.SPECIAL_MISSIONS),
    Case(SACCases.PRISON_BREAKOUT, 25, SACPlanets.PRISON_PLANET, SACOperatives.RATCHET),
    Case(SACCases.DAMS_EDGE_HYDRANO, 26, SACPlanets.HYDRANO, SACOperatives.SPECIAL_MISSIONS),
    # planet LOW CONFIDENCE; operative LOW CONFIDENCE — inferred from "Qwarkography Ch. 5" flavor text
    Case(SACCases.A_FICTION_FULL_OF_DOLLARS, 27, SACPlanets.HYDRANO, SACOperatives.QWARK),
    # planet LOW CONFIDENCE
    Case(SACCases.BULKHEAD_LOCK, 28, SACPlanets.FORT_SPROCKET, SACOperatives.GADGETBOTS),
    # operative LOW CONFIDENCE — inferred from Blackout Pen/Holo-Monocle (Clank gadgets) flavor text
    Case(SACCases.UNDERWATER_BUNKER, 29, SACPlanets.HYDRANO, SACOperatives.CLANK),
    # operative LOW CONFIDENCE — inferred from stealth-takedown-on-Klunk flavor text
    Case(SACCases.KLUNKS_LAIR, 30, SACPlanets.HYDRANO, SACOperatives.CLANK),
)

# Fixed display/iteration order -- first appearance in ALL_CASES.
PLANET_NAMES: tuple[str, ...] = tuple(dict.fromkeys(case.planet for case in ALL_CASES))
OPERATIVE_NAMES: tuple[str, ...] = tuple(dict.fromkeys(case.operative for case in ALL_CASES))

CASE_ID_TO_CASE: dict[int, Case] = {case.case_id: case for case in ALL_CASES}
# Separate from CASE_ID_TO_CASE -- see Case dataclass. Only covers cases
# with a confirmed menu_id so far (most are still None).
MENU_ID_TO_CASE: dict[int, Case] = {case.menu_id: case for case in ALL_CASES if case.menu_id is not None}
CASE_NAME_TO_CASE: dict[str, Case] = {case.name: case for case in ALL_CASES}
CASE_NAME_TO_PLANET: dict[str, str] = {case.name: case.planet for case in ALL_CASES}
CASE_NAME_TO_OPERATIVE: dict[str, str] = {case.name: case.operative for case in ALL_CASES}

CASES_BY_PLANET: dict[str, tuple[Case, ...]] = {
    planet: tuple(case for case in ALL_CASES if case.planet == planet) for planet in PLANET_NAMES
}
CASES_BY_OPERATIVE: dict[str, tuple[Case, ...]] = {
    operative: tuple(case for case in ALL_CASES if case.operative == operative) for operative in OPERATIVE_NAMES
}

# TODO: treated as the final case for the victory condition (see
# regions.py) -- confirm Klunk's Lair is really the last case before
# relying on this.
GOAL_CASE: Case = CASE_NAME_TO_CASE[SACCases.KLUNKS_LAIR]

# Display name -> the AP item that grants access to that planet's cases.
# One access item per planet, mirroring the infobot-per-planet pattern the
# other RaC worlds use — see items.py's PLANET_ACCESS_ITEM_TABLE. The
# starting planet (Boltaire Museum) has none -- it's always reachable, see
# rules.py.
PLANET_ACCESS_ITEM_NAME: dict[str, str] = {
    planet: f"{planet} Access" for planet in PLANET_NAMES[1:]
}

# Case.name -> the Case File item that grants access to that specific
# case -- SAC's own in-game term for these (not "Infobot", which is the
# other RaC worlds' naming). Finer-grained than PLANET_ACCESS_ITEM_NAME
# above -- used by rules.py to gate individual per-case locations (e.g.
# skill points, see locations.py's SKILL_POINT_LOCATION_TO_CASE) on top of
# the coarser planet-entrance gate. Includes the starting case (case_id 1,
# Boltaire Museum) too -- world.py's create_items() precollects its Case
# File unconditionally rather than special-casing it as "always true" in
# the rules, so it's a real starting-inventory item like any other.
CASE_NAME_TO_INFOBOT: dict[str, str] = {
    case.name: f"Case File: {case.name}" for case in ALL_CASES
}

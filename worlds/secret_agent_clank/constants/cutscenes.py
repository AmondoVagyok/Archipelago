"""String constants for cutscene-trigger locations (see options.py's
AllCutscenes). Backed by the same Completed-missions-style bitmask region
as constants/missions.py's story missions -- 0x206BE0-0x206BF4, called
STORY_PROGRESS in the old address-map comments since cutscenes and
missions turned out to share it. Each address covers several cutscenes,
not one-per-cutscene -- a cutscene is identified by the bit it sets in its
CaseStructure.event_address byte (see CaseStructure.event_flag) when it
fires. CONFIRMED live for every entry below.

Display names follow "{character/operative}: {case}: {description}" (user:
"can we actually change the layout to character: planet: description for
the cutscenes" -- "planet" here means the case name, e.g. "Rooftop
Deathtrap", matching how the Gadgetbots: Rooftop Deathtrap example was
given) -- which is exactly what CaseStructure.__str__ builds from
case_name + event_name, so only the short event_name needs to be hand-typed
per entry now."""

from dataclasses import dataclass

from .planets import SACCases
from .types import CaseStructure, group_by_case


@dataclass(frozen=True)
class SACCutscenes:
    """String constants for cutscene-trigger event titles (short form only
    -- see CUTSCENES below for which case/address/flag each belongs to)."""

    ENTER_CUTSCENE = "Enter Cutscene"
    COMPLETE_CASE_CUTSCENE = "Complete Case Cutscene"
    RESCURE_CLANK_CUTSCENE = "Rescure Clank Cutscene"
    GODZILLA_LAZER_BEAM = "Godzilla Lazer Beam"
    COMPLETE_CUTSCENE = "Complete Cutscene"
    ENTER_THE_MANSION = "Enter the mansion"
    COMPLETE_DANCE_CUTSCENE = "Complete Dance Cutscene"
    MEET_JACK_CUTSCENE = "Meet Jack Cutscene"
    FINISH_GONDOLA_CUTSCENE = "Finish Gondola Cutscene"
    DEFEAT_JACK_CUTSCENE = "Defeat Jack Cutscene"
    OPEN_GREEN_DOOR_CUTSCENE = "Open Green Door Cutscene"
    ENTERE_CUTSCENE = "Entere Cutscene"
    MID_FIGHT_CUTSCENE_FOR_ROBO_RATCHET = "Mid Fight Cutscene for Robo Ratchet"
    HIGH_IMPACT_GAMES_CUTSCENE_WITH_GIANT_CLANK = "High Impact Games Cutscene with Giant Clank"


# One CaseStructure per cutscene -- pairs each short SACCutscenes title
# with its case and its confirmed address/flag in the shared
# 0x206BE0-0x206BF4 bitmask region. Assigned to a name where a later entry
# (CUTSCENE_EXTRA_REQUIREMENTS below) needs to refer back to it.
_boltaire_gem_wing_complete = CaseStructure(
    SACCases.BOLTAIRE_GEM_WING, SACCutscenes.COMPLETE_CASE_CUTSCENE, event_flag=0b00000100, event_address=0x206BE0,
)

CUTSCENES: tuple[CaseStructure, ...] = (
    CaseStructure(SACCases.BOLTAIRE_MUSEUM, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BE0),
    _boltaire_gem_wing_complete,
    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00001000, event_address=0x206BE0),
    CaseStructure(SACCases.ROOFTOP_DEATHTRAP, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BE2),
    CaseStructure(
        SACCases.ROOFTOP_DEATHTRAP, SACCutscenes.RESCURE_CLANK_CUTSCENE, event_flag=0b00000010, event_address=0x206BE2,
    ),
    CaseStructure(SACCases.ASYANICA_ROOFTOPS, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000100, event_address=0x206BE2),
    CaseStructure(SACCases.LARGER_THAN_LIFE, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00001000, event_address=0x206BE2),
    CaseStructure(
        SACCases.LARGER_THAN_LIFE, SACCutscenes.GODZILLA_LAZER_BEAM, event_flag=0b00100000, event_address=0x206BE2,
    ),
    CaseStructure(SACCases.LARGER_THAN_LIFE, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00010000, event_address=0x206BE2),
    CaseStructure(SACCases.COUNTESS_VILLA, SACCutscenes.ENTER_THE_MANSION, event_flag=0b00000001, event_address=0x206BE4),
    CaseStructure(
        SACCases.COUNTESS_VILLA, SACCutscenes.COMPLETE_DANCE_CUTSCENE, event_flag=0b00000010, event_address=0x206BE4,
    ),
    CaseStructure(SACCases.THE_MESS_HALL, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000100, event_address=0x206BE4),
    CaseStructure(SACCases.AZCOTAL_ALLEY, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BE6),
    CaseStructure(SACCases.AZCOTAL_ALLEY, SACCutscenes.MEET_JACK_CUTSCENE, event_flag=0b00000010, event_address=0x206BE6),
    CaseStructure(
        SACCases.GONDOLA_ASCENT, SACCutscenes.FINISH_GONDOLA_CUTSCENE, event_flag=0b00000100, event_address=0x206BE6,
    ),
    CaseStructure(SACCases.SUCK_AND_JIVE, SACCutscenes.DEFEAT_JACK_CUTSCENE, event_flag=0b00010000, event_address=0x206BE6),
    CaseStructure(SACCases.HIGH_ROLLERS_CASINO, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BE8),
    CaseStructure(
        SACCases.HIGH_ROLLERS_CASINO, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000011, event_address=0x206BE8,
    ),
    CaseStructure(SACCases.THE_EXERCISE_YARD, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000100, event_address=0x206BE8),
    CaseStructure(SACCases.HIGH_STAKES_ROOM, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000110, event_address=0x206BE8),
    CaseStructure(SACCases.VENANTONIO_LABS, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BEA),
    CaseStructure(
        SACCases.VENANTONIO_LABS, SACCutscenes.OPEN_GREEN_DOOR_CUTSCENE, event_flag=0b00000010, event_address=0x206BEA,
    ),
    CaseStructure(SACCases.VENANTONIO_LABS, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000100, event_address=0x206BEA),
    CaseStructure(
        SACCases.VENANTONIO_CANALS, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00001000, event_address=0x206BEA,
    ),
    CaseStructure(SACCases.MADAM_BUTTERQWARK, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00010000, event_address=0x206BEA),
    CaseStructure(
        SACCases.MADAM_BUTTERQWARK, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00100000, event_address=0x206BEA,
    ),
    CaseStructure(
        SACCases.GALACTIC_BOLT_RESERVE, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BEC,
    ),
    CaseStructure(
        SACCases.GALACTIC_BOLT_RESERVE, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000010, event_address=0x206BEC,
    ),
    CaseStructure(
        SACCases.INSIDE_THE_A_EYE, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000100, event_address=0x206BEC,
    ),
    CaseStructure(SACCases.THE_SHOWERS, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00001000, event_address=0x206BEC),
    CaseStructure(
        SACCases.SPACESHIP_GRAVEYARD, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BEE,
    ),
    CaseStructure(
        SACCases.SPACESHIP_GRAVEYARD, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000010, event_address=0x206BEE,
    ),
    CaseStructure(SACCases.SAINT_QWARK, SACCutscenes.ENTERE_CUTSCENE, event_flag=0b00000100, event_address=0x206BEE),
    CaseStructure(SACCases.PRISON_BREAKOUT, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BF0),
    CaseStructure(SACCases.DAMS_EDGE_HYDRANO, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000010, event_address=0x206BF0),
    CaseStructure(
        SACCases.DAMS_EDGE_HYDRANO, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00000100, event_address=0x206BF0,
    ),
    CaseStructure(
        SACCases.A_FICTION_FULL_OF_DOLLARS, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00001000, event_address=0x206BF0,
    ),
    CaseStructure(
        SACCases.A_FICTION_FULL_OF_DOLLARS, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00010000, event_address=0x206BF0,
    ),
    CaseStructure(SACCases.BULKHEAD_LOCK, SACCutscenes.ENTER_CUTSCENE, event_flag=0b00000001, event_address=0x206BF2),
    CaseStructure(SACCases.KLUNKS_LAIR, SACCutscenes.ENTERE_CUTSCENE, event_flag=0b00000010, event_address=0x206BF2),
    CaseStructure(
        SACCases.KLUNKS_LAIR, SACCutscenes.MID_FIGHT_CUTSCENE_FOR_ROBO_RATCHET, event_flag=0b00000100,
        event_address=0x206BF2,
    ),
    CaseStructure(SACCases.KLUNKS_LAIR, SACCutscenes.COMPLETE_CUTSCENE, event_flag=0b00001000, event_address=0x206BF2),
    CaseStructure(
        SACCases.KLUNKS_LAIR, SACCutscenes.HIGH_IMPACT_GAMES_CUTSCENE_WITH_GIANT_CLANK, event_flag=0b00001100,
        event_address=0x206BF4,
    ),
)

@dataclass(frozen=True)
class SACCutsceneLocations:
    """One named constant per cutscene location -- each value is the exact
    full display name CUTSCENES above builds via CaseStructure.__str__
    (case + short SACCutscenes title), spelled out here so rules/<case>.py
    can reference an individual location directly (e.g.
    SACCutsceneLocations.BOLTAIRE_MUSEUM_ENTER_CUTSCENE) instead of a raw
    string or a case-name-keyed lookup -- same one-name-per-location layout
    as constants/weapons.py's SACRatchetWeapons."""

    BOLTAIRE_MUSEUM_ENTER_CUTSCENE = "Clank: Boltaire Museum: Enter Cutscene"
    BOLTAIRE_GEM_WING_COMPLETE_CASE_CUTSCENE = "Special Missions: Boltaire Gem Wing: Complete Case Cutscene"
    MAX_SECURITY_CELLS_ENTER_CUTSCENE = "Ratchet: Max-Security Cells: Enter Cutscene"
    ROOFTOP_DEATHTRAP_ENTER_CUTSCENE = "Gadgetbots: Rooftop Deathtrap: Enter Cutscene"
    ROOFTOP_DEATHTRAP_RESCURE_CLANK_CUTSCENE = "Gadgetbots: Rooftop Deathtrap: Rescure Clank Cutscene"
    ASYANICA_ROOFTOPS_ENTER_CUTSCENE = "Clank: Asyanica Rooftops: Enter Cutscene"
    LARGER_THAN_LIFE_ENTER_CUTSCENE = "Qwark: Larger Than Life: Enter Cutscene"
    LARGER_THAN_LIFE_GODZILLA_LAZER_BEAM = "Qwark: Larger Than Life: Godzilla Lazer Beam"
    LARGER_THAN_LIFE_COMPLETE_CUTSCENE = "Qwark: Larger Than Life: Complete Cutscene"
    COUNTESS_VILLA_ENTER_THE_MANSION = "Special Missions: Countess's Villa: Enter the mansion"
    COUNTESS_VILLA_COMPLETE_DANCE_CUTSCENE = "Special Missions: Countess's Villa: Complete Dance Cutscene"
    THE_MESS_HALL_ENTER_CUTSCENE = "Ratchet: The Mess Hall: Enter Cutscene"
    AZCOTAL_ALLEY_ENTER_CUTSCENE = "Clank: Azcotal Alley: Enter Cutscene"
    AZCOTAL_ALLEY_MEET_JACK_CUTSCENE = "Clank: Azcotal Alley: Meet Jack Cutscene"
    GONDOLA_ASCENT_FINISH_GONDOLA_CUTSCENE = "Clank: Gondola Ascent: Finish Gondola Cutscene"
    SUCK_AND_JIVE_DEFEAT_JACK_CUTSCENE = "Qwark: Suck and Jive: Defeat Jack Cutscene"
    HIGH_ROLLERS_CASINO_ENTER_CUTSCENE = "Clank: High-Rollers Casino: Enter Cutscene"
    HIGH_ROLLERS_CASINO_COMPLETE_CUTSCENE = "Clank: High-Rollers Casino: Complete Cutscene"
    THE_EXERCISE_YARD_COMPLETE_CUTSCENE = "Ratchet: The Exercise Yard: Complete Cutscene"
    HIGH_STAKES_ROOM_COMPLETE_CUTSCENE = "Special Missions: High Stakes Room: Complete Cutscene"
    VENANTONIO_LABS_ENTER_CUTSCENE = "Clank: Venantonio Labs: Enter Cutscene"
    VENANTONIO_LABS_OPEN_GREEN_DOOR_CUTSCENE = "Clank: Venantonio Labs: Open Green Door Cutscene"
    VENANTONIO_LABS_COMPLETE_CUTSCENE = "Clank: Venantonio Labs: Complete Cutscene"
    VENANTONIO_CANALS_COMPLETE_CUTSCENE = "Special Missions: Venantonio Canals: Complete Cutscene"
    MADAM_BUTTERQWARK_ENTER_CUTSCENE = "Qwark: Madam Butterqwark: Enter Cutscene"
    MADAM_BUTTERQWARK_COMPLETE_CUTSCENE = "Qwark: Madam Butterqwark: Complete Cutscene"
    GALACTIC_BOLT_RESERVE_ENTER_CUTSCENE = "Clank: Galactic Bolt Reserve: Enter Cutscene"
    GALACTIC_BOLT_RESERVE_COMPLETE_CUTSCENE = "Clank: Galactic Bolt Reserve: Complete Cutscene"
    INSIDE_THE_A_EYE_COMPLETE_CUTSCENE = "Gadgetbots: Inside the A-Eye: Complete Cutscene"
    THE_SHOWERS_ENTER_CUTSCENE = "Ratchet: The Showers: Enter Cutscene"
    SPACESHIP_GRAVEYARD_ENTER_CUTSCENE = "Clank: Spaceship Graveyard: Enter Cutscene"
    SPACESHIP_GRAVEYARD_COMPLETE_CUTSCENE = "Clank: Spaceship Graveyard: Complete Cutscene"
    SAINT_QWARK_ENTERE_CUTSCENE = "Qwark: Saint Qwark: Entere Cutscene"
    PRISON_BREAKOUT_ENTER_CUTSCENE = "Ratchet: Prison Breakout!: Enter Cutscene"
    DAMS_EDGE_HYDRANO_ENTER_CUTSCENE = "Special Missions: Dam's Edge, Hydrano: Enter Cutscene"
    DAMS_EDGE_HYDRANO_COMPLETE_CUTSCENE = "Special Missions: Dam's Edge, Hydrano: Complete Cutscene"
    A_FICTION_FULL_OF_DOLLARS_ENTER_CUTSCENE = "Qwark: A Fiction Full Of Dollars: Enter Cutscene"
    A_FICTION_FULL_OF_DOLLARS_COMPLETE_CUTSCENE = "Qwark: A Fiction Full Of Dollars: Complete Cutscene"
    BULKHEAD_LOCK_ENTER_CUTSCENE = "Gadgetbots: Bulkhead Lock: Enter Cutscene"
    KLUNKS_LAIR_ENTERE_CUTSCENE = "Clank: Klunk's Lair: Entere Cutscene"
    KLUNKS_LAIR_MID_FIGHT_CUTSCENE_FOR_ROBO_RATCHET = "Clank: Klunk's Lair: Mid Fight Cutscene for Robo Ratchet"
    KLUNKS_LAIR_COMPLETE_CUTSCENE = "Clank: Klunk's Lair: Complete Cutscene"
    KLUNKS_LAIR_HIGH_IMPACT_GAMES_CUTSCENE_WITH_GIANT_CLANK = "Clank: Klunk's Lair: High Impact Games Cutscene with Giant Clank"


# Cutscene full display name -> the case it belongs to, derived from
# CUTSCENES above -- kept for callers that want a flat name->case lookup
# instead of iterating CUTSCENES (locations.py, notably).
CUTSCENE_TO_CASE: dict[str, str] = {str(entry): entry.case_name for entry in CUTSCENES}

# Case name -> its cutscenes' full display names, same group_by_case shape
# as SKILL_POINTS_BY_CASE/ALIEN_CODES_BY_CASE -- lets rules/<case>.py
# reference these locations by constant instead of hand-typing them.
CUTSCENES_BY_CASE: dict[str, tuple[str, ...]] = group_by_case(CUTSCENES)

# Cutscene name -> extra item requirements beyond the case's own infobot
# gate (CASE_NAME_TO_INFOBOT in constants/planets.py). Item names are TODO
# -- ink pen, bowtie and jet boots don't exist as AP items yet (see
# constants/clank_gadgets.py, items.py); not wired into rules.py until they
# do.
CUTSCENE_EXTRA_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    str(_boltaire_gem_wing_complete): ("Ink Pen", "Bowtie", "Jet Boots"),
}

assert {v for k, v in vars(SACCutsceneLocations).items() if not k.startswith("_")} == set(CUTSCENE_TO_CASE), \
    "SACCutsceneLocations drifted out of sync with CUTSCENES -- regenerate its literals"

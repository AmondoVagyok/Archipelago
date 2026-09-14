"""String constants for story mission names -- the real per-case mission title, as opposed to locations.py's "{case.name} Complete" placeholder used until every mission has a real case/address (see core/missions.py)."""

from dataclasses import dataclass
from enum import IntFlag

from .gadgetbot_challenges import GADGETBOT_CHALLENGES
from .planets import ALL_CASES, SACCases
from .ratchet_challenges import RATCHET_CHALLENGES
from .special_challenges import SPECIAL_CHALLENGES
from .types import CaseStructure


@dataclass(frozen=True)
class SACMissions:
    """String constants for real story mission titles (short form only -- see CHAPTER_ENTRIES below for which case/address/flag each belongs to)."""

    ESCAPE_THE_RAVINE = "Escape The Ravine"
    GET_INSIDE_THE_MUSEUM = "Get Inside the Museum"
    NOT_THE_GUIDED_TOUR = "Not The Guided Tour"
    THE_NIGHT_FOX = "The Night Fox"
    LIFE_IN_PRISON = "Life in Prison"
    GET_A_CLUE = "Get a Clue"
    FREE_AGENT_CLANK = "Free Agent Clank!"
    NUMBER_WOO_WORKS_FOR_ME = "Number Woo works for ..."
    LARGER_THAN_LIFE = "Qwarkography, Ch. 1"
    TANGO_OF_100_SORROWS = "Tango of 100 Sorrows"
    BLACK_DIAMOND_OF_DOOM = "Black Diamond of Doom!"
    NO_TIME_FOR_SECONDS = "No Time for Seconds"
    THE_LUNCH_MENU_FOREVER = "The Lunch Menu Forever"
    THE_KINGPIN = "The Kingpin"
    ALL_THE_KINGPINS_MEN = "All the Kingpin's Men"
    GET_A_LIFT = "Get a Lift"
    SUCK_AND_JIVE = "Qwarkography, The Gamblin' Years"
    EXPLORE_PARADISE = "Explore Paradise"
    PARADISE_EXPLOITED = "Paradise Exploited"
    AND_THE_PASSWORD_IS = "And the Password is ..."
    FIGHT_FOR_SLIM = "Fight for Slim"
    HIGH_RISK_VS_HIGH_REWARD = "High Risk vs. High Reward"
    CRASHING_THE_PARTY = "Crashing the Party"
    OUT_OF_THE_FRYING_PAN = "Out of the Frying Pan"
    DANGER_OFF_STARBOARD = "Danger off Starboard!"
    MADAM_BUTTERQWARK = "Qwarkography, Ch. 3"
    HARD_CURRENCY = "Hard Currency"
    THE_BIG_HEIST = "The Big Heist"
    PAYBACKS_A_PUNCH = "Payback's a Punch"
    PLUMBING_TROUBLES = "Plumbing Troubles"
    RUB_A_DUB_DEATH = "Rub-a-Dub Death"
    TRACKING_THE_KINGPIN = "Tracking the Kingpin"
    SAINT_QWARK = "Qwarkography, Ch. 4"
    ESCAPE_THE_KUDZU = "Escape the Kudzu"
    THE_GREAT_ESCAPE = "The Great Escape"
    AND_NOW_JUSTICE_FOR_ALL = "And Now... Justice for All"
    SHIPS_SIGNAL = "Ship's Signal"
    FOLLOW_THAT_CAR = "Follow That Car"
    A_FICTION_FULL_OF_DOLLARS = "Qwarkography, Ch. 5"
    UNDERWATER_BASE = "Underwater Base"
    LOCKED_DOOR = "Locked Door"
    CLANK_UNDER_GLASS = "Clank Under Glass"
    ALL_THE_MARBLES = "All the Marbles"
    # Mission title matches its case name outright, same as
    # LARGER_THAN_LIFE/SUCK_AND_JIVE/MADAM_BUTTERQWARK/SAINT_QWARK/
    # A_FICTION_FULL_OF_DOLLARS above.
    KLUNKS_LAIR = "Klunk's Lair"
    HIGH_TREEHOUSE = "High Impact Treehouse"

    # Challenge/"Mega Challenge"-style missions -- only complete once every
    # challenge tied to them is done (see e.g. constants/ratchet_challenges.py's
    # *_MEGA_CHALLENGE_* entries).
    CONSECUTIVE_LIFE_SENTENCES = "Consecutive Life Sentences"
    THE_HALLS_OF_ASYANICA = "The Halls of Asyanica"
    PRO_BOARDING = "Pro Boarding"
    POWER_JET_BOATING = "Power Jet Boating"
    MYE_MYNDE_IS_GOING = "Mye Mynde is Going..."
    THE_DRIFT_KING = "The Drift King"
    INSULT_TO_INJURY = "Insult to Injury"

# CONFIRMED live values for a CHAPTER_ENTRIES entry's own address byte.
# ENABLED (1) is an unconfirmed intermediate state, kept as a distinct
# member in case it shows up; DISABLED (0), UNLOCKED (2), and
# UNLOCKED_COMPLETED (3) are the three states client code actually
# writes -- DISABLED to lock a mission, UNLOCKED to make one reachable
# without marking it complete (see /unlock, /lock, /unlock_all,
# /lock_all, and MissionInventory.enforce_owned_first_missions()),
# UNLOCKED_COMPLETED for an actual completion.
class MissionFlag(IntFlag):
    DISABLED = 0x0
    ENABLED = 0x1
    UNLOCKED = 0x2
    UNLOCKED_COMPLETED = 0x3

@dataclass
class SACMissionEntry:
    name: SACMissions
    address: int
    flag: MissionFlag = MissionFlag.DISABLED
    title_id: int = 0

    def __post_init__(self) -> None:
        # A property/setter pair here (instead of this) would collide with
        # the dataclass-generated __init__: the property definition
        # overwrites the field's default value in the class namespace
        # before @dataclass ever reads it, so every no-flag-given
        # construction (i.e. every CHAPTER_ENTRIES entry) would raise
        # instead of defaulting to MissionFlag.DISABLED.
        if not isinstance(self.flag, MissionFlag):
            raise ValueError(f"Expected a MissionFlag, got {type(self.flag)}")


# USA mission titles and title IDs decoded from the native string/mission tables.
# Native case labels split shared module slots. Addresses are resolved at runtime.
CHAPTER_ENTRIES = {
    SACCases.BOLTAIRE_MUSEUM: [
        SACMissionEntry(name="Escape the Ravine", address=0, title_id=5501),
        SACMissionEntry(name="Get Inside the Museum", address=0, title_id=5503),
        SACMissionEntry(name="Not The Guided Tour", address=0, title_id=5505),
    ],
    SACCases.BOLTAIRE_GEM_WING: [
        SACMissionEntry(name="The Night Fox", address=0, title_id=5507),
    ],
    SACCases.MAX_SECURITY_CELLS: [
        SACMissionEntry(name="Life In Prison", address=0, title_id=5509),
        SACMissionEntry(name="Consecutive Life Sentences", address=0, title_id=5511),
    ],
    SACCases.ROOFTOP_DEATHTRAP: [
        SACMissionEntry(name="Get A Clue", address=0, title_id=5513),
        SACMissionEntry(name="Free Agent Clank!", address=0, title_id=5515),
        SACMissionEntry(name="The Halls of Asyanica", address=0, title_id=5517),
    ],
    SACCases.ASYANICA_ROOFTOPS: [
        SACMissionEntry(name="Number Woo works for...?", address=0, title_id=5519),
    ],
    SACCases.LARGER_THAN_LIFE: [
        SACMissionEntry(name="Qwarkography, Ch. 1", address=0, title_id=5521),
    ],
    SACCases.COUNTESS_VILLA: [
        SACMissionEntry(name="Tango of 100 Sorrows", address=0, title_id=5523),
    ],
    SACCases.GLACIARA_SKI_SLOPES: [
        SACMissionEntry(name="Black Diamond of Doom!", address=0, title_id=5525),
        SACMissionEntry(name="Pro Boarding", address=0, title_id=5591),
    ],
    SACCases.THE_MESS_HALL: [
        SACMissionEntry(name="No Time for Seconds", address=0, title_id=5527),
        SACMissionEntry(name="The Lunch Menu Forever", address=0, title_id=5529),
    ],
    SACCases.AZCOTAL_ALLEY: [
        SACMissionEntry(name="The Kingpin", address=0, title_id=5531),
        SACMissionEntry(name="All The Kingpin's Men", address=0, title_id=5533),
    ],
    SACCases.GONDOLA_ASCENT: [
        SACMissionEntry(name="Get A Lift", address=0, title_id=5535),
    ],
    SACCases.SUCK_AND_JIVE: [
        SACMissionEntry(name="Qwarkography, The Gamblin' Years", address=0, title_id=5537),
    ],
    SACCases.HIGH_ROLLERS_CASINO: [
        SACMissionEntry(name="Explore Paradise", address=0, title_id=5539),
        SACMissionEntry(name="Paradise Exploited", address=0, title_id=5541),
    ],
    SACCases.THE_EXERCISE_YARD: [
        SACMissionEntry(name="And the password is...", address=0, title_id=5543),
        SACMissionEntry(name="Fight for Slim", address=0, title_id=5545),
    ],
    SACCases.HIGH_STAKES_ROOM: [
        SACMissionEntry(name="High Risk vs. High Stakes", address=0, title_id=5547),
    ],
    SACCases.VENANTONIO_LABS: [
        SACMissionEntry(name="Crashing the Party", address=0, title_id=5549),
        SACMissionEntry(name="Out of the Frying Pan...", address=0, title_id=5551),
    ],
    SACCases.VENANTONIO_CANALS: [
        SACMissionEntry(name="Danger off Starboard", address=0, title_id=5553),
        SACMissionEntry(name="Power Jet Boating", address=0, title_id=5593),
    ],
    SACCases.MADAM_BUTTERQWARK: [
        SACMissionEntry(name="Qwarkography, Ch. 3", address=0, title_id=5555),
    ],
    SACCases.GALACTIC_BOLT_RESERVE: [
        SACMissionEntry(name="Hard Currency", address=0, title_id=5557),
        SACMissionEntry(name="The Big Heist", address=0, title_id=5559),
    ],
    SACCases.INSIDE_THE_A_EYE: [
        SACMissionEntry(name="Payback's a Punch", address=0, title_id=5561),
        SACMissionEntry(name="Mye Mynde Is Going...", address=0, title_id=5597),
    ],
    SACCases.THE_SHOWERS: [
        SACMissionEntry(name="Plumbing Troubles", address=0, title_id=5563),
        SACMissionEntry(name="Rub-a-dub-death", address=0, title_id=5565),
    ],
    SACCases.SPACESHIP_GRAVEYARD: [
        SACMissionEntry(name="Tracking the Kingpin", address=0, title_id=5567),
    ],
    SACCases.SAINT_QWARK: [
        SACMissionEntry(name="Qwarkography, Ch. 4", address=0, title_id=5569),
    ],
    SACCases.THE_QUASAR_FIELDS: [
        SACMissionEntry(name="Escape the Kudzu", address=0, title_id=5571),
    ],
    SACCases.PRISON_BREAKOUT: [
        SACMissionEntry(name="The Great Escape", address=0, title_id=5573),
        SACMissionEntry(name="And Now... Justice For All", address=0, title_id=5575),
    ],
    SACCases.DAMS_EDGE_HYDRANO: [
        SACMissionEntry(name="Ship's signal", address=0, title_id=5579),
        SACMissionEntry(name="Follow that Car!", address=0, title_id=5577),
        SACMissionEntry(name="The Drift King", address=0, title_id=5595),
    ],
    SACCases.A_FICTION_FULL_OF_DOLLARS: [
        SACMissionEntry(name="Qwarkography, Ch. 5", address=0, title_id=5581),
    ],
    SACCases.BULKHEAD_LOCK: [
        SACMissionEntry(name="Underwater Base", address=0, title_id=5583),
        SACMissionEntry(name="Locked Door", address=0, title_id=5585),
        SACMissionEntry(name="Insult to Injury", address=0, title_id=5599),
    ],
    SACCases.UNDERWATER_BUNKER: [
        SACMissionEntry(name="Clank under glass", address=0, title_id=5587),
    ],
    SACCases.KLUNKS_LAIR: [
        SACMissionEntry(name="All The Marbles", address=0, title_id=5589),
    ],
    SACCases.HIGH_TREEHOUSE: [
        SACMissionEntry(name="The HIG Treehouse", address=0, title_id=5636),
    ],
}

# Flat (case_name, SACMissionEntry) pairs from CHAPTER_ENTRIES, in
# declaration order -- for core/missions.py's MissionInventory and client
# debug commands that need to walk every mission regardless of case.
ALL_CHAPTER_ENTRIES: tuple[tuple[str, SACMissionEntry], ...] = tuple(
    (case_name, entry) for case_name, entries in CHAPTER_ENTRIES.items() for entry in entries
)

# Mission full name -> the case it belongs to. CHAPTER_ENTRIES is the
# actual mission tracker now (see its comment above), so this is derived
# from it directly rather than the old MISSIONS/CaseStructure table.
MISSION_TO_CASE: dict[str, str] = {entry.name: case_name for case_name, entry in ALL_CHAPTER_ENTRIES}

# Mission full name -> its SACMissionEntry (address + flag), for O(1)
# lookup by name -- e.g. client debug commands that write a single
# mission's flag byte directly rather than walking the whole table.
MISSION_NAME_TO_CHAPTER_ENTRY: dict[str, SACMissionEntry] = {
    entry.name: entry for _, entry in ALL_CHAPTER_ENTRIES
}


@dataclass(frozen=True)
class SACMissionLocations:
    """One named constant per story mission location -- both granularities options.py's Missions can produce: an individual CHAPTER_ENTRIES mission (all) and the coarser "{case} Complete" placeholder (level_completion, the default) -- so rules/<case>.py can reference either directly instead of a raw string."""

    BOLTAIRE_MUSEUM_ESCAPE_THE_RAVINE = "Mission: Escape the Ravine"
    BOLTAIRE_MUSEUM_GET_INSIDE_THE_MUSEUM = "Mission: Get Inside the Museum"
    BOLTAIRE_MUSEUM_NOT_THE_GUIDED_TOUR = "Mission: Not The Guided Tour"
    BOLTAIRE_GEM_WING_THE_NIGHT_FOX = "Mission: The Night Fox"
    MAX_SECURITY_CELLS_LIFE_IN_PRISON = "Mission: Life In Prison"
    MAX_SECURITY_CELLS_CONSECUTIVE_LIFE_SENTENCES = "Mission: Consecutive Life Sentences"
    ROOFTOP_DEATHTRAP_GET_A_CLUE = "Mission: Get A Clue"
    ROOFTOP_DEATHTRAP_FREE_AGENT_CLANK = "Mission: Free Agent Clank!"
    ROOFTOP_DEATHTRAP_THE_HALLS_OF_ASYANICA = "Mission: The Halls of Asyanica"
    LARGER_THAN_LIFE_QWARKOGRAPHY_CH_1 = "Mission: Qwarkography, Ch. 1"
    COUNTESS_VILLA_TANGO_OF_100_SORROWS = "Mission: Tango of 100 Sorrows"
    ASYANICA_ROOFTOPS_NUMBER_WOO_WORKS_FOR = "Mission: Number Woo works for...?"
    GLACIARA_SKI_SLOPES_BLACK_DIAMOND_OF_DOOM = "Mission: Black Diamond of Doom!"
    GLACIARA_SKI_SLOPES_PRO_BOARDING = "Mission: Pro Boarding"
    THE_MESS_HALL_NO_TIME_FOR_SECONDS = "Mission: No Time for Seconds"
    THE_MESS_HALL_THE_LUNCH_MENU_FOREVER = "Mission: The Lunch Menu Forever"
    AZCOTAL_ALLEY_THE_KINGPIN = "Mission: The Kingpin"
    AZCOTAL_ALLEY_ALL_THE_KINGPIN_S_MEN = "Mission: All The Kingpin's Men"
    GONDOLA_ASCENT_GET_A_LIFT = "Mission: Get A Lift"
    SUCK_AND_JIVE_QWARKOGRAPHY_THE_GAMBLIN_YEARS = "Mission: Qwarkography, The Gamblin' Years"
    HIGH_ROLLERS_CASINO_EXPLORE_PARADISE = "Mission: Explore Paradise"
    HIGH_ROLLERS_CASINO_PARADISE_EXPLOITED = "Mission: Paradise Exploited"
    THE_EXERCISE_YARD_AND_THE_PASSWORD_IS = "Mission: And the password is..."
    THE_EXERCISE_YARD_FIGHT_FOR_SLIM = "Mission: Fight for Slim"
    HIGH_STAKES_ROOM_HIGH_RISK_VS_HIGH_STAKES = "Mission: High Risk vs. High Stakes"
    VENANTONIO_LABS_CRASHING_THE_PARTY = "Mission: Crashing the Party"
    VENANTONIO_LABS_OUT_OF_THE_FRYING_PAN = "Mission: Out of the Frying Pan..."
    VENANTONIO_CANALS_DANGER_OFF_STARBOARD = "Mission: Danger off Starboard"
    VENANTONIO_CANALS_POWER_JET_BOATING = "Mission: Power Jet Boating"
    MADAM_BUTTERQWARK_QWARKOGRAPHY_CH_3 = "Mission: Qwarkography, Ch. 3"
    GALACTIC_BOLT_RESERVE_HARD_CURRENCY = "Mission: Hard Currency"
    GALACTIC_BOLT_RESERVE_THE_BIG_HEIST = "Mission: The Big Heist"
    INSIDE_THE_A_EYE_PAYBACK_S_A_PUNCH = "Mission: Payback's a Punch"
    INSIDE_THE_A_EYE_MYE_MYNDE_IS_GOING = "Mission: Mye Mynde Is Going..."
    THE_SHOWERS_PLUMBING_TROUBLES = "Mission: Plumbing Troubles"
    THE_SHOWERS_RUB_A_DUB_DEATH = "Mission: Rub-a-dub-death"
    SPACESHIP_GRAVEYARD_TRACKING_THE_KINGPIN = "Mission: Tracking the Kingpin"
    SAINT_QWARK_QWARKOGRAPHY_CH_4 = "Mission: Qwarkography, Ch. 4"
    THE_QUASAR_FIELDS_ESCAPE_THE_KUDZU = "Mission: Escape the Kudzu"
    PRISON_BREAKOUT_THE_GREAT_ESCAPE = "Mission: The Great Escape"
    PRISON_BREAKOUT_AND_NOW_JUSTICE_FOR_ALL = "Mission: And Now... Justice For All"
    DAMS_EDGE_HYDRANO_SHIP_S_SIGNAL = "Mission: Ship's signal"
    DAMS_EDGE_HYDRANO_FOLLOW_THAT_CAR = "Mission: Follow that Car!"
    DAMS_EDGE_HYDRANO_THE_DRIFT_KING = "Mission: The Drift King"
    A_FICTION_FULL_OF_DOLLARS_QWARKOGRAPHY_CH_5 = "Mission: Qwarkography, Ch. 5"
    BULKHEAD_LOCK_UNDERWATER_BASE = "Mission: Underwater Base"
    BULKHEAD_LOCK_LOCKED_DOOR = "Mission: Locked Door"
    BULKHEAD_LOCK_INSULT_TO_INJURY = "Mission: Insult to Injury"
    UNDERWATER_BUNKER_CLANK_UNDER_GLASS = "Mission: Clank under glass"
    KLUNKS_LAIR_ALL_THE_MARBLES = "Mission: All The Marbles"

    BOLTAIRE_MUSEUM_COMPLETE = "Mission: Boltaire Museum Complete"
    BOLTAIRE_GEM_WING_COMPLETE = "Mission: Boltaire Gem Wing Complete"
    MAX_SECURITY_CELLS_COMPLETE = "Mission: Max-Security Cells Complete"
    ROOFTOP_DEATHTRAP_COMPLETE = "Mission: Rooftop Deathtrap Complete"
    LARGER_THAN_LIFE_COMPLETE = "Mission: Larger Than Life Complete"
    COUNTESS_VILLA_COMPLETE = "Mission: Countess's Villa Complete"
    ASYANICA_ROOFTOPS_COMPLETE = "Mission: Asyanica Rooftops Complete"
    GLACIARA_SKI_SLOPES_COMPLETE = "Mission: Glaciara, Ski Slopes Complete"
    THE_MESS_HALL_COMPLETE = "Mission: The Mess Hall Complete"
    AZCOTAL_ALLEY_COMPLETE = "Mission: Azcotal Alley Complete"
    GONDOLA_ASCENT_COMPLETE = "Mission: Gondola Ascent Complete"
    SUCK_AND_JIVE_COMPLETE = "Mission: Suck and Jive Complete"
    HIGH_ROLLERS_CASINO_COMPLETE = "Mission: High-Rollers Casino Complete"
    THE_EXERCISE_YARD_COMPLETE = "Mission: The Exercise Yard Complete"
    HIGH_STAKES_ROOM_COMPLETE = "Mission: High Stakes Room Complete"
    VENANTONIO_LABS_COMPLETE = "Mission: Venantonio Labs Complete"
    VENANTONIO_CANALS_COMPLETE = "Mission: Venantonio Canals Complete"
    MADAM_BUTTERQWARK_COMPLETE = "Mission: Madam Butterqwark Complete"
    GALACTIC_BOLT_RESERVE_COMPLETE = "Mission: Galactic Bolt Reserve Complete"
    INSIDE_THE_A_EYE_COMPLETE = "Mission: Inside the A-Eye Complete"
    THE_SHOWERS_COMPLETE = "Mission: The Showers Complete"
    SPACESHIP_GRAVEYARD_COMPLETE = "Mission: Spaceship Graveyard Complete"
    SAINT_QWARK_COMPLETE = "Mission: Saint Qwark Complete"
    THE_QUASAR_FIELDS_COMPLETE = "Mission: The Quasar Fields Complete"
    PRISON_BREAKOUT_COMPLETE = "Mission: Prison Breakout! Complete"
    DAMS_EDGE_HYDRANO_COMPLETE = "Mission: Dam's Edge, Hydrano Complete"
    A_FICTION_FULL_OF_DOLLARS_COMPLETE = "Mission: A Fiction Full Of Dollars Complete"
    BULKHEAD_LOCK_COMPLETE = "Mission: Bulkhead Lock Complete"
    UNDERWATER_BUNKER_COMPLETE = "Mission: Underwater Bunker Complete"
    KLUNKS_LAIR_COMPLETE = "Mission: Klunk's Lair Complete"

assert {v for k, v in vars(SACMissionLocations).items() if not k.startswith("_")} == (
    {f"Mission: {entry.name}" for case in ALL_CASES for entry in CHAPTER_ENTRIES.get(case.name, ())}
    | {f"Mission: {case.name} Complete" for case in ALL_CASES}
), "SACMissionLocations drifted out of sync with CHAPTER_ENTRIES/ALL_CASES -- regenerate its literals"

# Every challenge CaseStructure, by full display name -- the lookup for
# gadgetbot/special/ratchet challenges (unrelated to CHAPTER_ENTRIES
# above -- those are still bitflag-tracked via core/case_events.py). All
# three challenge types share the same pine, so no separate Inventory
# instance is needed to read them -- just the CaseStructure entries
# themselves (case/address/flag).
CHALLENGE_BY_NAME: dict[str, CaseStructure] = {
    str(entry): entry for entry in (*GADGETBOT_CHALLENGES, *SPECIAL_CHALLENGES, *RATCHET_CHALLENGES)
}


"""Ratchet arena challenge names in native per-case challenge order."""

from dataclasses import dataclass

from .planets import SACCases
from .types import CaseStructure, group_by_case


@dataclass(frozen=True)
class SACRatchetChallenges:
    """String constants for Ratchet Challenge event titles (short form only -- see RATCHET_CHALLENGES below for which case/address each belongs to)."""

    CATCH_AS_CATCH_CAN = "Catch-as-Catch-Can"
    AMOEBOID_ON_A_POLE = "Amoeboid on a Pole"
    IRON_MAN = "Iron Man"
    TRIPLE_THREAT = "Triple Threat"
    MEGA_CHALLENGE_BATTLE_ROYAL = "Mega Challenge: Battle Royal"

    LAST_ONE_PICKED_FOR_DODGEBALL = "Last One Picked For Dodgeball"
    STEEL_IS_STEEL = "Steel Is Steel"
    PUMPING_IRON_MOLTEN_IRON = "Pumping Iron. Molten Iron."
    GREAT_BALLS_OF_FIRE = "Great Balls Of Fire!"
    MEGA_CHALLENGE_PRISON_YARD = "Mega Challenge: Prison Yard"

    NAILS_FOR_BREAKFAST = "Nails for Breakfast"
    TYHRRANOID_RECYCLING = "Tyhrranoid Recycling"
    ITS_RAINING_PHLEGM_HALLELUJAH = "It's Raining Phlegm! Hallelujah!"
    MEATLOAF_TUESDAYS = "Meatloaf Tuesdays"
    MEGA_CHALLENGE_CAFETERIA = "Mega Challenge: Cafeteria"

    NO_GOOD_DEED_GOES_UNPUNISHED = "No good deed goes unpunished."
    COVER_YOUR_SHAME = "Cover Your Shame!"
    DIDNT_NEED_TO_SEE_THAT = "Didn't need to see that!"
    ITS_A_DRY_HEAT = "It's a Dry Heat"
    MEGA_CHALLENGE_SHOWER = "Mega Challenge: Shower"

    KARMIC_BREAKDOWN = "Karmic Breakdown"
    NO_SHELTER = "No Shelter"
    PAST_DUE = "Past Due"
    SPEAK_SOFTLY_AND = "Speak Softly And.."
    MEGA_CHALLENGE_CELLBLOCK = "Mega Challenge: Cellblock"


_CATEGORY = "Ratchet Challenge"

RATCHET_CHALLENGES: tuple[CaseStructure, ...] = (
    CaseStructure(
        SACCases.PRISON_BREAKOUT, SACRatchetChallenges.CATCH_AS_CATCH_CAN, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C54,
    ),
    CaseStructure(
        SACCases.PRISON_BREAKOUT, SACRatchetChallenges.AMOEBOID_ON_A_POLE, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C55,
    ),
    CaseStructure(
        SACCases.PRISON_BREAKOUT, SACRatchetChallenges.IRON_MAN, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C56,
    ),
    CaseStructure(
        SACCases.PRISON_BREAKOUT, SACRatchetChallenges.TRIPLE_THREAT, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C57,
    ),
    CaseStructure(
        SACCases.PRISON_BREAKOUT, SACRatchetChallenges.MEGA_CHALLENGE_BATTLE_ROYAL, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C58,
    ),

    CaseStructure(
        SACCases.THE_EXERCISE_YARD, SACRatchetChallenges.LAST_ONE_PICKED_FOR_DODGEBALL, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C44,
    ),
    CaseStructure(
        SACCases.THE_EXERCISE_YARD, SACRatchetChallenges.STEEL_IS_STEEL, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C45,
    ),
    CaseStructure(
        SACCases.THE_EXERCISE_YARD, SACRatchetChallenges.PUMPING_IRON_MOLTEN_IRON, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C46,
    ),
    CaseStructure(
        SACCases.THE_EXERCISE_YARD, SACRatchetChallenges.GREAT_BALLS_OF_FIRE, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C47,
    ),
    CaseStructure(
        SACCases.THE_EXERCISE_YARD, SACRatchetChallenges.MEGA_CHALLENGE_PRISON_YARD, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C48,
    ),

    CaseStructure(
        SACCases.THE_MESS_HALL, SACRatchetChallenges.NAILS_FOR_BREAKFAST, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C3C,
    ),
    CaseStructure(
        SACCases.THE_MESS_HALL, SACRatchetChallenges.TYHRRANOID_RECYCLING, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C3D,
    ),
    CaseStructure(
        SACCases.THE_MESS_HALL, SACRatchetChallenges.ITS_RAINING_PHLEGM_HALLELUJAH, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C3E,
    ),
    CaseStructure(
        SACCases.THE_MESS_HALL, SACRatchetChallenges.MEATLOAF_TUESDAYS, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C3F,
    ),
    CaseStructure(
        SACCases.THE_MESS_HALL, SACRatchetChallenges.MEGA_CHALLENGE_CAFETERIA, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C40,
    ),

    CaseStructure(
        SACCases.THE_SHOWERS, SACRatchetChallenges.NO_GOOD_DEED_GOES_UNPUNISHED, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C4C,
    ),
    CaseStructure(
        SACCases.THE_SHOWERS, SACRatchetChallenges.COVER_YOUR_SHAME, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C4D,
    ),
    CaseStructure(
        SACCases.THE_SHOWERS, SACRatchetChallenges.DIDNT_NEED_TO_SEE_THAT, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C4E,
    ),
    CaseStructure(
        SACCases.THE_SHOWERS, SACRatchetChallenges.ITS_A_DRY_HEAT, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C4F,
    ),
    CaseStructure(
        SACCases.THE_SHOWERS, SACRatchetChallenges.MEGA_CHALLENGE_SHOWER, _CATEGORY,
        event_flag=0b00000001, event_address=0x206C50,
    ),

    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACRatchetChallenges.KARMIC_BREAKDOWN, _CATEGORY),
    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACRatchetChallenges.NO_SHELTER, _CATEGORY),
    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACRatchetChallenges.PAST_DUE, _CATEGORY),
    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACRatchetChallenges.SPEAK_SOFTLY_AND, _CATEGORY),
    CaseStructure(SACCases.MAX_SECURITY_CELLS, SACRatchetChallenges.MEGA_CHALLENGE_CELLBLOCK, _CATEGORY),
)

# Case.name -> its known Ratchet Challenges' full display names, derived
# from RATCHET_CHALLENGES above. Order is declaration order (display/
# iteration order) and matches native challenge indices within each case.
RATCHET_CHALLENGES_BY_CASE: dict[str, tuple[str, ...]] = group_by_case(RATCHET_CHALLENGES)


@dataclass(frozen=True)
class SACRatchetChallengeLocations:
    """One named constant per Ratchet Challenge location -- each value is the exact full display name RATCHET_CHALLENGES above builds via CaseStructure.__str__, spelled out here so rules/<case>.py can reference an individual location directly -- same one-name-per-location layout as constants/weapons.py's SACRatchetWeapons."""

    PRISON_BREAKOUT_CATCH_AS_CATCH_CAN = "Ratchet: Prison Breakout!: Ratchet Challenge: Catch-as-Catch-Can"
    PRISON_BREAKOUT_AMOEBOID_ON_A_POLE = "Ratchet: Prison Breakout!: Ratchet Challenge: Amoeboid on a Pole"
    PRISON_BREAKOUT_IRON_MAN = "Ratchet: Prison Breakout!: Ratchet Challenge: Iron Man"
    PRISON_BREAKOUT_TRIPLE_THREAT = "Ratchet: Prison Breakout!: Ratchet Challenge: Triple Threat"
    PRISON_BREAKOUT_MEGA_CHALLENGE_BATTLE_ROYAL = "Ratchet: Prison Breakout!: Ratchet Challenge: Mega Challenge: Battle Royal"
    THE_EXERCISE_YARD_LAST_ONE_PICKED_FOR_DODGEBALL = "Ratchet: The Exercise Yard: Ratchet Challenge: Last One Picked For Dodgeball"
    THE_EXERCISE_YARD_STEEL_IS_STEEL = "Ratchet: The Exercise Yard: Ratchet Challenge: Steel Is Steel"
    THE_EXERCISE_YARD_PUMPING_IRON_MOLTEN_IRON = "Ratchet: The Exercise Yard: Ratchet Challenge: Pumping Iron. Molten Iron."
    THE_EXERCISE_YARD_GREAT_BALLS_OF_FIRE = "Ratchet: The Exercise Yard: Ratchet Challenge: Great Balls Of Fire!"
    THE_EXERCISE_YARD_MEGA_CHALLENGE_PRISON_YARD = "Ratchet: The Exercise Yard: Ratchet Challenge: Mega Challenge: Prison Yard"
    THE_MESS_HALL_NAILS_FOR_BREAKFAST = "Ratchet: The Mess Hall: Ratchet Challenge: Nails for Breakfast"
    THE_MESS_HALL_TYHRRANOID_RECYCLING = "Ratchet: The Mess Hall: Ratchet Challenge: Tyhrranoid Recycling"
    THE_MESS_HALL_ITS_RAINING_PHLEGM_HALLELUJAH = "Ratchet: The Mess Hall: Ratchet Challenge: It's Raining Phlegm! Hallelujah!"
    THE_MESS_HALL_MEATLOAF_TUESDAYS = "Ratchet: The Mess Hall: Ratchet Challenge: Meatloaf Tuesdays"
    THE_MESS_HALL_MEGA_CHALLENGE_CAFETERIA = "Ratchet: The Mess Hall: Ratchet Challenge: Mega Challenge: Cafeteria"
    THE_SHOWERS_NO_GOOD_DEED_GOES_UNPUNISHED = "Ratchet: The Showers: Ratchet Challenge: No good deed goes unpunished."
    THE_SHOWERS_COVER_YOUR_SHAME = "Ratchet: The Showers: Ratchet Challenge: Cover Your Shame!"
    THE_SHOWERS_DIDNT_NEED_TO_SEE_THAT = "Ratchet: The Showers: Ratchet Challenge: Didn't need to see that!"
    THE_SHOWERS_ITS_A_DRY_HEAT = "Ratchet: The Showers: Ratchet Challenge: It's a Dry Heat"
    THE_SHOWERS_MEGA_CHALLENGE_SHOWER = "Ratchet: The Showers: Ratchet Challenge: Mega Challenge: Shower"
    MAX_SECURITY_CELLS_KARMIC_BREAKDOWN = "Ratchet: Max-Security Cells: Ratchet Challenge: Karmic Breakdown"
    MAX_SECURITY_CELLS_NO_SHELTER = "Ratchet: Max-Security Cells: Ratchet Challenge: No Shelter"
    MAX_SECURITY_CELLS_PAST_DUE = "Ratchet: Max-Security Cells: Ratchet Challenge: Past Due"
    MAX_SECURITY_CELLS_SPEAK_SOFTLY_AND = "Ratchet: Max-Security Cells: Ratchet Challenge: Speak Softly And.."
    MAX_SECURITY_CELLS_MEGA_CHALLENGE_CELLBLOCK = "Ratchet: Max-Security Cells: Ratchet Challenge: Mega Challenge: Cellblock"

assert {v for k, v in vars(SACRatchetChallengeLocations).items() if not k.startswith("_")} == set(
    str(entry) for entry in RATCHET_CHALLENGES
), "SACRatchetChallengeLocations drifted out of sync with RATCHET_CHALLENGES -- regenerate its literals"

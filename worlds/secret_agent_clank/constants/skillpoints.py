"""Skill point locations and their native completion flags (all 65 confirmed live)."""
from dataclasses import dataclass

from .types import EventFlag


@dataclass(frozen=True)
class SACSkillPointLocations:
    BOLTAIRE_MUSEUM_FURIOUS_FISTS = "Boltaire (Clank) - Boltaire Museum: Skill Point: Furious Fists of Fury"
    BOLTAIRE_MUSEUM_SILENT_NIGHT = "Boltaire (Clank) - Boltaire Museum: Skill Point: Silent Night"
    BOLTAIRE_GEM_WING_PYRRHIC_VICTORY = "Boltaire (Special Missions) - Boltaire Gem Wing: Skill Point: Pyrrhic Victory"
    BOLTAIRE_GEM_WING_TRIPLE_PLATINUM = "Boltaire (Special Missions) - Boltaire Gem Wing: Skill Point: Triple Platinum Record"
    MAX_SECURITY_CELLS_STAINLESS_STEEL = "Prison Planet (Ratchet) - Max-Security Cells: Skill Point: Stainless Steel"
    MAX_SECURITY_CELLS_PLAYING_WITH_FIRE = "Prison Planet (Ratchet) - Max-Security Cells: Skill Point: Playing With Fire"
    ROOFTOP_DEATHTRAP_SPEED_DEMON = "Asyanica (Gadgetbots) - Rooftop Deathtrap: Skill Point: Speed Demon"
    ROOFTOP_DEATHTRAP_PERFECT_CHROME_FINISH = "Asyanica (Gadgetbots) - Rooftop Deathtrap: Skill Point: Perfect Chrome Finish"
    ASYANICA_ROOFTOPS_ROBOT_FINDS_NINJA = "Asyanica (Clank) - Asyanica Rooftops: Skill Point: Robot Finds Ninja"
    ASYANICA_ROOFTOPS_BLACK_TIE_AFFAIR = "Asyanica (Clank) - Asyanica Rooftops: Skill Point: Black Tie Affair"
    ASYANICA_ROOFTOPS_LIKE_THE_WIND = "Asyanica (Clank) - Asyanica Rooftops: Skill Point: Like The Wind"
    LARGER_THAN_LIFE_INVERSE_NINJA_LAW = "Asyanica (Qwark) - Larger Than Life: Skill Point: Inverse Ninja Law"
    LARGER_THAN_LIFE_BLASTER_OVERLOAD = "Asyanica (Qwark) - Larger Than Life: Skill Point: Blaster Overload"
    COUNTESS_VILLA_PERFECT_TANGO = "Glaciara (Special Missions) - Countess's Villa: Skill Point: Perfect Tango"
    GLACIARA_SKI_SLOPES_BLACK_DIAMOND = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Skill Point: Black Diamond"
    GLACIARA_SKI_SLOPES_SMOOTH_MOVES = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Skill Point: Smooth Moves"
    GLACIARA_SKI_SLOPES_RINGLEADER = "Glaciara (Special Missions) - Glaciara, Ski Slopes: Skill Point: Ringleader"
    THE_MESS_HALL_EMPTY_THE_WARRENS = "Prison Planet (Ratchet) - The Mess Hall: Skill Point: Empty The Warrens"
    THE_MESS_HALL_ANTAEUS = "Prison Planet (Ratchet) - The Mess Hall: Skill Point: Antaeus"
    AZCOTAL_ALLEY_MASTER_OF_DISGUISE = "Rionosis (Clank) - Azcotal Alley: Skill Point: Master of Disguise"
    AZCOTAL_ALLEY_TRASH_TALK = "Rionosis (Clank) - Azcotal Alley: Skill Point: Trash Talk"
    AZCOTAL_ALLEY_DEADLY_HANDS = "Rionosis (Clank) - Azcotal Alley: Skill Point: Deadly Hands"
    GONDOLA_ASCENT_STEEL_RAIN = "Rionosis (Clank) - Gondola Ascent: Skill Point: Steel Rain"
    SUCK_AND_JIVE_CARD_PICKUP = "Rionosis (Qwark) - Suck and Jive: Skill Point: 52 Card Pickup"
    SUCK_AND_JIVE_DRESS_FOR_SUCCESS = "Rionosis (Qwark) - Suck and Jive: Skill Point: Dress For Success"
    HIGH_ROLLERS_CASINO_BEAT_THE_HOUSE = "The Paradis Des Tricheurs Casino (Clank) - High-Rollers Casino: Skill Point: Beat The House"
    THE_EXERCISE_YARD_INDIAN_BURN = "Prison Planet (Ratchet) - The Exercise Yard: Skill Point: Indian Burn"
    THE_EXERCISE_YARD_LAW_CANT_TOUCH_ME = "Prison Planet (Ratchet) - The Exercise Yard: Skill Point: The Law Can't Touch Me"
    HIGH_STAKES_ROOM_LUCKY_SEVENS = "The Paradis Des Tricheurs Casino (Special Missions) - High Stakes Room: Skill Point: Lucky Sevens"
    HIGH_STAKES_ROOM_GADGEBOT_STANDS_ALONE = "The Paradis Des Tricheurs Casino (Special Missions) - High Stakes Room: Skill Point: A Gadgebot Stands Alone"
    VENANTONIO_LABS_ALL_SLIME_MUST_BURN = "Venantonio (Clank) - Venantonio Labs: Skill Point: All Slime Must Burn"
    VENANTONIO_LABS_RAMMING_SPEED = "Venantonio (Clank) - Venantonio Labs: Skill Point: Ramming Speed!"
    VENANTONIO_CANALS_EVASIVE_MANEUVERS = "Venantonio (Special Missions) - Venantonio Canals: Skill Point: Evasive Maneuvers"
    VENANTONIO_CANALS_DEEP_SIX = "Venantonio (Special Missions) - Venantonio Canals: Skill Point: Deep Six"
    VENANTONIO_CANALS_WAKE_OF_DESTRUCTION = "Venantonio (Special Missions) - Venantonio Canals: Skill Point: Wake Of Destruction"
    VENANTONIO_CANALS_RINGMASTER = "Venantonio (Special Missions) - Venantonio Canals: Skill Point: Ringmaster"
    MADAM_BUTTERQWARK_TWINKLE_TOES = "Venantonio (Qwark) - Madam Butterqwark: Skill Point: Twinkle Toes"
    MADAM_BUTTERQWARK_MAGNUM_OPUS = "Venantonio (Qwark) - Madam Butterqwark: Skill Point: Magnum Opus"
    MADAM_BUTTERQWARK_SOLD_OUT = "Venantonio (Qwark) - Madam Butterqwark: Skill Point: Sold Out"
    GALACTIC_BOLT_RESERVE_WITH_INTEREST = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Skill Point: With Interest"
    GALACTIC_BOLT_RESERVE_ANDROIDS_IN_DISGUISE = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Skill Point: Androids In Disguise"
    GALACTIC_BOLT_RESERVE_VAULT_VAULT = "Fort Sprocket (Clank) - Galactic Bolt Reserve: Skill Point: Vault Vault"
    INSIDE_THE_A_EYE_DIA_DE_LOS_MUERTOS = "Fort Sprocket (Gadgetbots) - Inside the A-Eye: Skill Point: El Día de los Muertos"
    THE_SHOWERS_RUBA_DUB_CLUB = "Prison Planet (Ratchet) - The Showers: Skill Point: Ruba-Dub Club"
    THE_SHOWERS_MODESTY = "Prison Planet (Ratchet) - The Showers: Skill Point: Modesty"
    SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE = "Spaceship Graveyard (Clank) - Spaceship Graveyard: Skill Point: It's A Delicacy Somewhere"
    SPACESHIP_GRAVEYARD_REVENANT = "Spaceship Graveyard (Clank) - Spaceship Graveyard: Skill Point: Revenant"
    SAINT_QWARK_PUNCHY = "Spaceship Graveyard (Qwark) - Saint Qwark: Skill Point: Punchy"
    SAINT_QWARK_SOUR_VICTORY = "Spaceship Graveyard (Qwark) - Saint Qwark: Skill Point: Sour Victory"
    THE_QUASAR_FIELDS_MIN_MAXING = "Spaceship Graveyard (Special Missions) - The Quasar Fields: Skill Point: Min Maxing"
    THE_QUASAR_FIELDS_KILL_THE_ROCK = "Spaceship Graveyard (Special Missions) - The Quasar Fields: Skill Point: I Kill the Rock"
    PRISON_BREAKOUT_WHIP_IT_GOOD = "Prison Planet (Ratchet) - Prison Breakout!: Skill Point: Whip It Good"
    PRISON_BREAKOUT_HANGING_JUDGE = "Prison Planet (Ratchet) - Prison Breakout!: Skill Point: Hanging Judge"
    DAMS_EDGE_HYDRANO_YEEE_HAAAAAW = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Skill Point: Yeeee Haaaaaw!"
    DAMS_EDGE_HYDRANO_OFFENSIVE_DRIVER = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Skill Point: Offensive Driver"
    DAMS_EDGE_HYDRANO_SLIPPERY_SLOPE = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Skill Point: Slippery Slope"
    DAMS_EDGE_HYDRANO_RING_AROUND_THE_ROSIE = "Hydrano (Special Missions) - Dam's Edge, Hydrano: Skill Point: Ring Around the Rosie"
    A_FICTION_FULL_OF_DOLLARS_CLEANS_POOLS_TOO = "Hydrano (Qwark) - A Fiction Full Of Dollars: Skill Point: He Cleans pools, Too!"
    A_FICTION_FULL_OF_DOLLARS_PERFECT_MIRROR = "Hydrano (Qwark) - A Fiction Full Of Dollars: Skill Point: Perfect Mirror"
    BULKHEAD_LOCK_CEREAL_DECODER_RING = "Hydrano (Gadgetbots) - Bulkhead Lock: Skill Point: Cerial Decoder Rung"
    UNDERWATER_BUNKER_LEET_HAXXOR = "Hydrano (Clank) - Underwater Bunker: Skill Point: I33t h4XX0r"
    UNDERWATER_BUNKER_RUST_PROOF = "Hydrano (Clank) - Underwater Bunker: Skill Point: Rust Proof"
    UNDERWATER_BUNKER_IM_NOT_THERE = "Hydrano (Clank) - Underwater Bunker: Skill Point: I'm not There"
    KLUNKS_LAIR_TURN_THE_TABLES = "Hydrano (Clank) - Klunk's Lair: Skill Point: Turn The Tables"
    KLUNKS_LAIR_PRETTY_GOOD_LIKENESS = "Hydrano (Clank) - Klunk's Lair: Skill Point: A Pretty Good Likeness"


# Flags walk 0x206BF8-0x206C00 one bit at a time, in case_id order.
SKILL_POINT_FLAGS: dict[str, EventFlag] = {
    SACSkillPointLocations.BOLTAIRE_MUSEUM_FURIOUS_FISTS: EventFlag(0x206BF8, 0b00000001),
    SACSkillPointLocations.BOLTAIRE_MUSEUM_SILENT_NIGHT: EventFlag(0x206BF8, 0b00000010),
    SACSkillPointLocations.BOLTAIRE_GEM_WING_PYRRHIC_VICTORY: EventFlag(0x206BF8, 0b00000100),
    SACSkillPointLocations.BOLTAIRE_GEM_WING_TRIPLE_PLATINUM: EventFlag(0x206BF8, 0b00001000),
    SACSkillPointLocations.MAX_SECURITY_CELLS_STAINLESS_STEEL: EventFlag(0x206BF8, 0b00010000),
    SACSkillPointLocations.MAX_SECURITY_CELLS_PLAYING_WITH_FIRE: EventFlag(0x206BF8, 0b00100000),
    SACSkillPointLocations.ROOFTOP_DEATHTRAP_SPEED_DEMON: EventFlag(0x206BF8, 0b01000000),
    SACSkillPointLocations.ROOFTOP_DEATHTRAP_PERFECT_CHROME_FINISH: EventFlag(0x206BF8, 0b10000000),
    SACSkillPointLocations.ASYANICA_ROOFTOPS_ROBOT_FINDS_NINJA: EventFlag(0x206BF9, 0b00000001),
    SACSkillPointLocations.ASYANICA_ROOFTOPS_BLACK_TIE_AFFAIR: EventFlag(0x206BF9, 0b00000010),
    SACSkillPointLocations.ASYANICA_ROOFTOPS_LIKE_THE_WIND: EventFlag(0x206BF9, 0b00000100),
    SACSkillPointLocations.LARGER_THAN_LIFE_INVERSE_NINJA_LAW: EventFlag(0x206BF9, 0b00001000),
    SACSkillPointLocations.LARGER_THAN_LIFE_BLASTER_OVERLOAD: EventFlag(0x206BF9, 0b00010000),
    SACSkillPointLocations.COUNTESS_VILLA_PERFECT_TANGO: EventFlag(0x206BF9, 0b00100000),
    SACSkillPointLocations.GLACIARA_SKI_SLOPES_BLACK_DIAMOND: EventFlag(0x206BF9, 0b01000000),
    SACSkillPointLocations.GLACIARA_SKI_SLOPES_SMOOTH_MOVES: EventFlag(0x206BF9, 0b10000000),
    SACSkillPointLocations.GLACIARA_SKI_SLOPES_RINGLEADER: EventFlag(0x206BFA, 0b00000001),
    SACSkillPointLocations.THE_MESS_HALL_EMPTY_THE_WARRENS: EventFlag(0x206BFA, 0b00000010),
    SACSkillPointLocations.THE_MESS_HALL_ANTAEUS: EventFlag(0x206BFA, 0b00000100),
    SACSkillPointLocations.AZCOTAL_ALLEY_MASTER_OF_DISGUISE: EventFlag(0x206BFA, 0b00001000),
    SACSkillPointLocations.AZCOTAL_ALLEY_TRASH_TALK: EventFlag(0x206BFA, 0b00010000),
    SACSkillPointLocations.AZCOTAL_ALLEY_DEADLY_HANDS: EventFlag(0x206BFA, 0b00100000),
    SACSkillPointLocations.GONDOLA_ASCENT_STEEL_RAIN: EventFlag(0x206BFA, 0b01000000),
    SACSkillPointLocations.SUCK_AND_JIVE_CARD_PICKUP: EventFlag(0x206BFA, 0b10000000),
    SACSkillPointLocations.SUCK_AND_JIVE_DRESS_FOR_SUCCESS: EventFlag(0x206BFB, 0b00000001),
    SACSkillPointLocations.HIGH_ROLLERS_CASINO_BEAT_THE_HOUSE: EventFlag(0x206BFB, 0b00000010),
    SACSkillPointLocations.THE_EXERCISE_YARD_INDIAN_BURN: EventFlag(0x206BFB, 0b00000100),
    SACSkillPointLocations.THE_EXERCISE_YARD_LAW_CANT_TOUCH_ME: EventFlag(0x206BFB, 0b00001000),
    SACSkillPointLocations.HIGH_STAKES_ROOM_LUCKY_SEVENS: EventFlag(0x206BFB, 0b00010000),
    SACSkillPointLocations.HIGH_STAKES_ROOM_GADGEBOT_STANDS_ALONE: EventFlag(0x206BFB, 0b00100000),
    SACSkillPointLocations.VENANTONIO_LABS_ALL_SLIME_MUST_BURN: EventFlag(0x206BFB, 0b01000000),
    SACSkillPointLocations.VENANTONIO_LABS_RAMMING_SPEED: EventFlag(0x206BFB, 0b10000000),
    SACSkillPointLocations.VENANTONIO_CANALS_EVASIVE_MANEUVERS: EventFlag(0x206BFC, 0b00000001),
    SACSkillPointLocations.VENANTONIO_CANALS_DEEP_SIX: EventFlag(0x206BFC, 0b00000010),
    SACSkillPointLocations.VENANTONIO_CANALS_WAKE_OF_DESTRUCTION: EventFlag(0x206BFC, 0b00000100),
    SACSkillPointLocations.VENANTONIO_CANALS_RINGMASTER: EventFlag(0x206BFC, 0b00001000),
    SACSkillPointLocations.MADAM_BUTTERQWARK_TWINKLE_TOES: EventFlag(0x206BFC, 0b00010000),
    SACSkillPointLocations.MADAM_BUTTERQWARK_MAGNUM_OPUS: EventFlag(0x206BFC, 0b00100000),
    SACSkillPointLocations.MADAM_BUTTERQWARK_SOLD_OUT: EventFlag(0x206BFC, 0b01000000),
    SACSkillPointLocations.GALACTIC_BOLT_RESERVE_WITH_INTEREST: EventFlag(0x206BFC, 0b10000000),
    SACSkillPointLocations.GALACTIC_BOLT_RESERVE_ANDROIDS_IN_DISGUISE: EventFlag(0x206BFD, 0b00000001),
    SACSkillPointLocations.GALACTIC_BOLT_RESERVE_VAULT_VAULT: EventFlag(0x206BFD, 0b00000010),
    SACSkillPointLocations.INSIDE_THE_A_EYE_DIA_DE_LOS_MUERTOS: EventFlag(0x206BFD, 0b00000100),
    SACSkillPointLocations.THE_SHOWERS_RUBA_DUB_CLUB: EventFlag(0x206BFD, 0b00001000),
    SACSkillPointLocations.THE_SHOWERS_MODESTY: EventFlag(0x206BFD, 0b00010000),
    SACSkillPointLocations.SPACESHIP_GRAVEYARD_DELICACY_SOMEWHERE: EventFlag(0x206BFD, 0b00100000),
    SACSkillPointLocations.SPACESHIP_GRAVEYARD_REVENANT: EventFlag(0x206BFD, 0b01000000),
    SACSkillPointLocations.SAINT_QWARK_PUNCHY: EventFlag(0x206BFD, 0b10000000),
    SACSkillPointLocations.SAINT_QWARK_SOUR_VICTORY: EventFlag(0x206BFE, 0b00000001),
    SACSkillPointLocations.THE_QUASAR_FIELDS_MIN_MAXING: EventFlag(0x206BFE, 0b00000010),
    SACSkillPointLocations.THE_QUASAR_FIELDS_KILL_THE_ROCK: EventFlag(0x206BFE, 0b00000100),
    SACSkillPointLocations.PRISON_BREAKOUT_WHIP_IT_GOOD: EventFlag(0x206BFE, 0b00001000),
    SACSkillPointLocations.PRISON_BREAKOUT_HANGING_JUDGE: EventFlag(0x206BFE, 0b00010000),
    SACSkillPointLocations.DAMS_EDGE_HYDRANO_YEEE_HAAAAAW: EventFlag(0x206BFE, 0b00100000),
    SACSkillPointLocations.DAMS_EDGE_HYDRANO_OFFENSIVE_DRIVER: EventFlag(0x206BFE, 0b01000000),
    SACSkillPointLocations.DAMS_EDGE_HYDRANO_SLIPPERY_SLOPE: EventFlag(0x206BFE, 0b10000000),
    SACSkillPointLocations.DAMS_EDGE_HYDRANO_RING_AROUND_THE_ROSIE: EventFlag(0x206BFF, 0b00000001),
    SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_CLEANS_POOLS_TOO: EventFlag(0x206BFF, 0b00000010),
    SACSkillPointLocations.A_FICTION_FULL_OF_DOLLARS_PERFECT_MIRROR: EventFlag(0x206BFF, 0b00000100),
    SACSkillPointLocations.BULKHEAD_LOCK_CEREAL_DECODER_RING: EventFlag(0x206BFF, 0b00001000),
    SACSkillPointLocations.UNDERWATER_BUNKER_LEET_HAXXOR: EventFlag(0x206BFF, 0b00010000),
    SACSkillPointLocations.UNDERWATER_BUNKER_RUST_PROOF: EventFlag(0x206BFF, 0b00100000),
    SACSkillPointLocations.UNDERWATER_BUNKER_IM_NOT_THERE: EventFlag(0x206BFF, 0b01000000),
    SACSkillPointLocations.KLUNKS_LAIR_TURN_THE_TABLES: EventFlag(0x206BFF, 0b10000000),
    SACSkillPointLocations.KLUNKS_LAIR_PRETTY_GOOD_LIKENESS: EventFlag(0x206C00, 0b00000001),
}

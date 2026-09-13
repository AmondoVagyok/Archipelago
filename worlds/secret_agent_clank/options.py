from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    ItemDict,
    OptionCounter,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .constants.cheats import TRAP_DURATIONS
from .constants.operatives import ALL_OPERATIVES


class Missions(Choice):
    """Controls the granularity of story-mission location checks.
    level_completion: one location per case -- "{Case} Complete", checked
    when that case's final CHAPTER_ENTRIES mission completes.
    all: one location per individual mission within each case (see
    constants/missions.py's CHAPTER_ENTRIES), checked as each one
    completes rather than only the last."""
    display_name = "Missions"
    option_level_completion = 0
    option_all = 1
    default = 0


class AllCutscenes(Toggle):
    """Include cutscene/flag-triggered events as location checks."""
    display_name = "All Cutscenes"


class SkillPoints(Toggle):
    """Include skill point challenges as location checks."""
    display_name = "Skill Points"


class AllKeycards(Toggle):
    """Include the 3 keycard pickups as optional AP location checks.
    This does not select or restrict the goal. The Chalice of Power goal
    can be played with this option on or off."""
    display_name = "All Keycards"


class AllAlienCodes(Toggle):
    """Include the 27 Alien Codes as optional AP location checks.
    This does not select or restrict the goal. Selecting Alien Codes under
    Goal requires collecting all 27, whether these location checks are on or off."""
    display_name = "All Alien Codes"


class Infobots(Choice):
    """Choose how access is unlocked.
    Planets: one access item unlocks a planet's cases.
    Cases: individual Case Files unlock individual cases.
    Progressive Planet: each copy unlocks the next planet in order.
    Character Unlocks: Ratchet/Clank unlock together per character;
    Qwark/Gadgetbots unlock one case per progressive copy.
    """
    display_name = "Infobots"
    option_planets = 0
    option_cases = 1
    option_progressive_planet = 2
    option_character_unlocks = 3
    default = 1


class Operatives(OptionCounter):
    """Enabled operatives (Ratchet, Clank, Qwark, Gadgetbots, and Special
    Missions -- user: "lets change characters to Operatives. we will have
    special missions here aswel as an operative"). Set one to 0 (or remove
    it) to remove it entirely from the game -- none of its cases are
    generated as locations at all, and their content is skipped ("their
    missions will not unlock"). Additional logic around this (e.g.
    redirecting their story beats) isn't implemented yet.

    Keys are operative names, not AP item names -- this isn't an ItemDict,
    it doesn't pick a subset of the item pool, it's a set of operative
    toggles regions.py reads to decide which cases even get created (see
    SACOperatives). Special Missions has no dedicated playable character of
    its own, but is still a real, independently toggleable group here --
    see constants/operatives.py's module docstring."""
    display_name = "Operatives"
    min = 0
    max = 1
    valid_keys = ALL_OPERATIVES
    default = dict.fromkeys(ALL_OPERATIVES, 1)

    def __init__(self, value: dict[str, int]) -> None:
        # Cull 0s so "set to 0" and "removed from the list" both collapse
        # to "key absent from .value" -- matches ItemDict's convention,
        # which regions.py's disabled_operatives relies on.
        value = {name: amount for name, amount in value.items() if amount != 0}
        super().__init__(value)


class Goal(Choice):
    """Victory condition.
    defeat_klunk: complete the Klunk's Lair case (the main story finale).
    qwark_opera: complete every case filed under the Qwark Operative group
    (see constants/operatives.py's SACOperatives -- Larger Than Life, Suck
    and Jive, and the other Qwark-tagged cases).
    any: victory as soon as either condition above is met.
    chalice_of_power: collect the Chalice of Power after obtaining the keycards.
    alien_codes: collect all 27 Alien Codes.
    all_gadgetbots: complete every case filed under the Gadgetbots Operative
    group (Rooftop Deathtrap, Inside the A-Eye, Bulkhead Lock).
    ratchet_prison_escape: complete every Ratchet Challenge location across
    all 5 Ratchet-operative prison cases (see constants/ratchet_challenges.py).
    Keycard and Alien Code location toggles are independent of these goals."""
    display_name = "Goal"
    option_defeat_klunk    = 0
    option_qwark_opera     = 1
    option_any             = 2
    option_chalice_of_power = 3
    option_alien_codes      = 4
    option_all_gadgetbots   = 5
    option_ratchet_prison_escape = 6
    default = 0


class NgPlus(Range):
    """New Game Plus level: 0 is the base game, 1 is NG+, and 2 is NG++."""
    display_name = "NG+"
    range_start = 0
    range_end = 2
    default = 0


class ProgressiveWeapons(Toggle):
    """AP weapon copies grant V1, then one level each. Combat does not level
    weapons in this mode. NG+ allows V5-V8; RYNO stops at V4."""
    display_name = "Progressive Weapons"


class ProgressiveWrench(Toggle):
    """Adds 5 Progressive Wrench items to the pool (Ratchet only) -- each
    copy upgrades the wrench a level. Off by default."""
    display_name = "Progressive Wrench"


class WeaponXPMultiplier(Range):
    """Combat weapon XP multiplier. Inactive with Progressive Weapons on."""
    display_name = "Weapon XP Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class HealthXPMultiplier(Range):
    """Multiplier for native health experience gains."""
    display_name = "Health XP Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class BoltMultiplier(Range):
    """Multiplier for earned bolts. Purchases and AP percentage rewards are unchanged."""
    display_name = "Bolt Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class DeathAmnesty(Range):
    """Number of deaths allowed before items are stripped from the player's
    inventory on death. Higher values are more forgiving."""
    display_name = "Death Amnesty"
    range_start = 0
    range_end = 5
    default = 0


class StartingWeapons(Range):
    """Number of random Ratchet weapons the player begins the game with."""
    display_name = "Starting Weapons"
    range_start = 0
    range_end = 4
    default = 1


class StartingGadgets(Range):
    """Number of random Clank spy gadgets the player begins the game with."""
    display_name = "Starting Gadgets"
    range_start = 0
    range_end = 3
    default = 1


class StartingBolts(Range):
    """Number of bolts the player begins the game with."""
    display_name = "Starting Bolts"
    range_start = 0
    range_end = 100_000
    default = 5_000


class TrapChance(Range):
    """Percent chance for each filler item to be replaced with a trap instead of Bolts."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeight(ItemDict):
    """Sets the relative weights of trap types in the filler pool. A higher value increases
    how often that trap is chosen over the others when a filler item rolls as a trap (see
    Trap Chance). Has no effect when Trap Chance is 0, or when every weight here is 0
    (Bolts fills in instead)."""
    display_name = "Trap Weight"
    min = 0
    max = 100
    valid_keys = TRAP_DURATIONS.keys()
    default = dict.fromkeys(TRAP_DURATIONS.keys(), 1)


class TrapDuration(OptionCounter):
    """How many seconds each trap type stays active once triggered."""
    display_name = "Trap Duration"
    min = 1
    max = 300
    valid_keys = TRAP_DURATIONS.keys()
    default = dict(TRAP_DURATIONS)


@dataclass
class SecretAgentClankOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_amnesty: DeathAmnesty
    all_missions: Missions
    all_cutscenes: AllCutscenes
    skill_points: SkillPoints
    all_keycards: AllKeycards
    all_alien_codes: AllAlienCodes
    goal: Goal
    infobots: Infobots
    operatives: Operatives
    ng_plus: NgPlus
    progressive_weapons: ProgressiveWeapons
    progressive_wrench: ProgressiveWrench
    weapon_xp_multiplier: WeaponXPMultiplier
    health_xp_multiplier: HealthXPMultiplier
    bolt_multiplier: BoltMultiplier
    starting_weapons: StartingWeapons
    starting_gadgets: StartingGadgets
    starting_bolts: StartingBolts
    trap_chance: TrapChance
    trap_weight: TrapWeight
    trap_duration: TrapDuration


sac_option_groups = [
    OptionGroup("SAC Item Options", [
        ProgressiveWeapons,
        ProgressiveWrench,
        WeaponXPMultiplier,
        HealthXPMultiplier,
        BoltMultiplier,
        StartingWeapons,
        StartingGadgets,
        StartingBolts,
        TrapChance,
        TrapWeight,
        TrapDuration,
    ]),
    OptionGroup("SAC Location Options", [
        Missions,
        AllCutscenes,
        SkillPoints,
        AllKeycards,
        AllAlienCodes,
        Goal,
        NgPlus,
    ]),
    OptionGroup("SAC Character Options", [
        Infobots,
        Operatives,
    ]),
]

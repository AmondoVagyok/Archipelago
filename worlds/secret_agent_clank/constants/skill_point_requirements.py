"""Wiki-backed ownership and curated difficulty; see docs/skill-points.md.

Native save grouping is not necessarily the case in which a point is earned.
Keep these gameplay requirements separate from skillpoints.py's memory records.
"""
from dataclasses import dataclass
from enum import IntEnum

from .operatives import SACOperatives
from .planets import CASE_NAME_TO_OPERATIVE, SACCases
from .skillpoints import SKILL_POINTS, SACSkillPoints as SP


class SkillPointDifficulty(IntEnum):
    EASY = 1
    HARD = 2


# Easy favors short/repeatable actions and forgiving weapon restrictions.
# Hard includes perfect runs, exhaustive objectives, tight timing and score goals.
EASY_SKILL_POINTS = frozenset({
    SP.FURIOUS_FISTS, SP.PLAYING_WITH_FIRE, SP.BLACK_TIE_AFFAIR,
    SP.INVERSE_NINJA_LAW, SP.BLASTER_OVERLOAD, SP.SMOOTH_MOVES,
    SP.STEEL_RAIN, SP.CARD_PICKUP, SP.DRESS_FOR_SUCCESS, SP.INDIAN_BURN,
    SP.ALL_SLIME_MUST_BURN, SP.RAMMING_SPEED, SP.EVASIVE_MANEUVERS,
    SP.WITH_INTEREST, SP.ANDROIDS_IN_DISGUISE, SP.DIA_DE_LOS_MUERTOS,
    SP.RUBA_DUB_CLUB, SP.PUNCHY, SP.SOUR_VICTORY, SP.KILL_THE_ROCK,
    SP.WHIP_IT_GOOD, SP.YEEE_HAAAAAW, SP.SLIPPERY_SLOPE,
    SP.CLEANS_POOLS_TOO, SP.RUST_PROOF, SP.TURN_THE_TABLES,
    SP.PRETTY_GOOD_LIKENESS,
})
HARD_SKILL_POINTS = frozenset({
    SP.SILENT_NIGHT, SP.PYRRHIC_VICTORY, SP.TRIPLE_PLATINUM,
    SP.STAINLESS_STEEL, SP.SPEED_DEMON, SP.PERFECT_CHROME_FINISH,
    SP.ROBOT_FINDS_NINJA, SP.LIKE_THE_WIND, SP.PERFECT_TANGO,
    SP.BLACK_DIAMOND, SP.RINGLEADER, SP.EMPTY_THE_WARRENS, SP.ANTAEUS,
    SP.MASTER_OF_DISGUISE, SP.TRASH_TALK, SP.DEADLY_HANDS,
    SP.BEAT_THE_HOUSE, SP.LAW_CANT_TOUCH_ME, SP.LUCKY_SEVENS,
    SP.GADGEBOT_STANDS_ALONE, SP.DEEP_SIX, SP.WAKE_OF_DESTRUCTION,
    SP.RINGMASTER, SP.TWINKLE_TOES, SP.MAGNUM_OPUS, SP.SOLD_OUT,
    SP.VAULT_VAULT, SP.MODESTY, SP.DELICACY_SOMEWHERE, SP.REVENANT,
    SP.MIN_MAXING, SP.HANGING_JUDGE, SP.OFFENSIVE_DRIVER,
    SP.RING_AROUND_THE_ROSIE, SP.PERFECT_MIRROR, SP.CEREAL_DECODER_RING,
    SP.LEET_HAXXOR, SP.IM_NOT_THERE,
})


@dataclass(frozen=True)
class SkillPointRequirement:
    difficulty: SkillPointDifficulty
    case: str
    operatives: frozenset[str]


def _requirement(point) -> SkillPointRequirement:
    # Vaultbreakers is a Gadgetbot challenge, despite the native save grouping.
    case = SACCases.INSIDE_THE_A_EYE if point.event_name == SP.VAULT_VAULT else point.case_name
    operatives = {CASE_NAME_TO_OPERATIVE[case]}
    if point.event_name == SP.GADGEBOT_STANDS_ALONE:
        # Embedded Gadgetbot combat sections of the casino rhythm mission.
        operatives.add(SACOperatives.GADGETBOTS)
    difficulty = (SkillPointDifficulty.EASY if point.event_name in EASY_SKILL_POINTS
                  else SkillPointDifficulty.HARD)
    return SkillPointRequirement(difficulty, case, frozenset(operatives))


SKILL_POINT_REQUIREMENTS = {str(point): _requirement(point) for point in SKILL_POINTS}

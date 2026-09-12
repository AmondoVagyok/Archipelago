"""String constants for the game's own "Operatives" grouping (Ratchet /
Clank / Gadgetbots / Qwark / Special Missions) -- confirmed real from the
in-game menu (user-supplied screenshots), a completely different axis from
Planet: a case belongs to exactly one Operative group AND one Planet (see
constants/planets.py's Case dataclass).

ALL_OPERATIVES is every group, including Special Missions -- options.py's
Operatives option (user: "lets change characters to Operatives. we will
have special missions here aswel as an operative") toggles all five, not
just the four playable characters. Special Missions has no dedicated
character of its own (it's a grab-bag of vehicle/rhythm-minigame sections
played as whichever character the mission's cutscene puts you in), which is
why CHARACTER_ITEM_NAME/PROGRESSIVE_CHARACTER_ITEM_NAME below -- the
per-operative unlock items for Infobots=character_unlocks -- still only
cover the other four; rule_helpers.py's case_access_rule() exempts Special
Missions cases from that specific per-case unlock-item gate for the same
reason, even though the Operatives option can now enable/disable its cases
outright same as any other operative (see regions.py's disabled_operatives())."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SACOperatives:
    """String constants for each Operatives group."""

    RATCHET = "Ratchet"
    CLANK = "Clank"
    GADGETBOTS = "Gadgetbots"
    QWARK = "Qwark"
    SPECIAL_MISSIONS = "Special Missions"


ALL_OPERATIVES: tuple[str, ...] = (
    SACOperatives.RATCHET, SACOperatives.CLANK, SACOperatives.QWARK,
    SACOperatives.GADGETBOTS, SACOperatives.SPECIAL_MISSIONS,
)

# Character Items option (see options.py): Ratchet/Clank unlock with one
# flat item each; Qwark/Gadgetbots are progressive instead (user: "progressive
# characters specifically for qwark and gadgetbots") -- each copy unlocks
# that character's next case in CASES_BY_OPERATIVE order (see
# constants/planets.py), rather than all-or-nothing. Special Missions has no
# entry in either table -- see module docstring.
CHARACTER_ITEM_NAME: dict[str, str] = {
    SACOperatives.RATCHET: "Play as Ratchet",
    SACOperatives.CLANK:   "Play as Clank",
}
PROGRESSIVE_CHARACTER_ITEM_NAME: dict[str, str] = {
    SACOperatives.QWARK:      "Progressive Qwark",
    SACOperatives.GADGETBOTS: "Progressive Gadgetbots",
}

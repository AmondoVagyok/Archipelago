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

# Infobots=character_unlocks: Ratchet and Clank unlock with one item each. Each
# Qwark/Gadgetbots copy unlocks that operative's next case in CASES_BY_OPERATIVE
# order. Special Missions cases need no character item.
CHARACTER_ITEM_NAME: dict[str, str] = {
    SACOperatives.RATCHET: "Play as Ratchet",
    SACOperatives.CLANK:   "Play as Clank",
}
PROGRESSIVE_CHARACTER_ITEM_NAME: dict[str, str] = {
    SACOperatives.QWARK:      "Progressive Qwark",
    SACOperatives.GADGETBOTS: "Progressive Gadgetbots",
}

from .option_choices import ClankSkinOptions as C, QwarkSkinOptions as Q, RatchetSkinOptions as R

RATCHET_SKINS = {
    "prison_scrubs": R.PRISON_SCRUBS,
    "towel": R.TOWEL,
    "super_incognito": R.SUPER_INCOGNITO,
    "tropical_vacation": R.TROPICAL_VACATION,
    "plundering_pirate_captain": R.PLUNDERING_PIRATE_CAPTAIN,
    "ratchetzilla": R.RATCHETZILLA,
    "kung_fu_ratchet": R.KUNG_FU_RATCHET,
    "zombie_ratchet": R.ZOMBIE_RATCHET,
    "dan": R.DAN,
}
CLANK_SKINS = {
    "suit": C.SUIT,
    "cowboy": C.COWBOY,
    "klunk": C.KLUNK,
    "70s_clank": C.CLANK_70S,
    "cop_clank": C.COP_CLANK,
    "blender": C.BLENDER,
    "zoni": C.ZONI,
}
QWARK_SKINS = {"regular": Q.REGULAR, "cowboy": Q.COWBOY, "maid_qwark": Q.MAID_QWARK,
               "lucha_libre_qwark": Q.LUCHA_LIBRE_QWARK}
QWARK_GIANT_SKINS = {18: 22, 19: 23, 20: 24, 21: 25}

SKIN_SAVE_OFFSET = 0x19900
SKIN_CHARACTER_STRIDE = 0x34
SKIN_OWNED_OFFSET = 0x199D4
UNSUPPORTED_RATCHET_SKIN = 7
DEFAULT_RATCHET_SKIN = 1
ALL_SKINS_MASK = sum(1 << skin for skin in range(1, 26) if skin != UNSUPPORTED_RATCHET_SKIN)
SKINS_BY_CHARACTER = {"ratchet": RATCHET_SKINS, "clank": CLANK_SKINS, "qwark": QWARK_SKINS}

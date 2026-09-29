"""USA PS2 SPHeroSkinId values, verified against the native skin menu."""

RATCHET_SKINS = {
    "prison_scrubs": 1,
    "towel": 2,
    "super_incognito": 3,
    "tropical_vacation": 4,
    "plundering_pirate_captain": 5,
    "ratchetzilla": 6,
    "robo_ratchet": 7,
    "kung_fu_ratchet": 8,
    "zombie_ratchet": 9,
    "dan": 10,
}
CLANK_SKINS = {
    "suit": 11,
    "cowboy": 12,
    "klunk": 13,
    "70s_clank": 14,
    "cop_clank": 15,
    "blender": 16,
    "zoni": 17,
}
QWARK_SKINS = {"regular": 18, "cowboy": 19, "maid_qwark": 20, "lucha_libre_qwark": 21}
QWARK_GIANT_SKINS = {18: 22, 19: 23, 20: 24, 21: 25}

# Save layout used by SelectedSPHeroSkinID and SCRNSKINSCREEN_Update.
SKIN_SAVE_OFFSET = 0x19900
SKIN_CHARACTER_STRIDE = 0x34
SKIN_OWNED_OFFSET = 0x199D4
ALL_SKINS_MASK = sum(1 << skin for skin in range(1, 26))
SKINS_BY_CHARACTER = {"ratchet": RATCHET_SKINS, "clank": CLANK_SKINS, "qwark": QWARK_SKINS}

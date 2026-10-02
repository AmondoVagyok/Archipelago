"""Slot layout of the native GadgetData array shared by Ratchet and Clank, and the internal slot names."""
from enum import IntEnum

# Index == native slot id. None marks a slot with no name (0 is blank, 1 is unnamed);
# those slots are never bound or tracked.
WEAPON_ORDER: list["str | None"] = [
    None,                          # slot 0   blank
    None,                          # slot 1   unknown/unnamed (category 2, no name)
    "blaster",                     # slot 2
    "shardgun",                    # slot 3
    "beemineglove",                # slot 4
    "shockrocket",                 # slot 5
    "walloper",                    # slot 6
    "plasmawhip",                  # slot 7
    "porkbomb",                    # slot 8
    "minelauncher",                # slot 9
    "ryno",                        # slot 10
    "throwTie",                    # slot 11
    "CuffLink",                    # slot 12
    "TangleVine",                  # slot 13
    "HoloKnuckles",                # slot 14
    "FlamethrowerPen",             # slot 15
    "LightningUmbrella",           # slot 16
    "fountainpen",                 # slot 17
    "hypnowatch",                  # slot 18
    "QwarkBlaster",                # slot 19
    "Vacuum",                      # slot 20
    "GiantQwarkBlaster",           # slot 21
    "hypershot",                   # slot 22   category 1 (tool/item, not a weapon)
    "ratchetpda",                  # slot 23   category 1
    "holomonocle",                 # slot 24   category 1
    "sunglasses",                  # slot 25   category 1
    "clankpda",                    # slot 26   category 1
    "bolttransfer",                # slot 27   category 3 (wrench ability)
    "wrenchpower_firebomb",        # slot 28   category 3
    "wrenchpower_triplewave",      # slot 29   category 3
    "wrenchpower_crystallix",      # slot 30   category 3
    "wrenchpower_wildburst",       # slot 31   category 3
    "jetboots",                    # slot 32   category 3
    "omnikey",                     # slot 33   category 3
    "mapomatic",                   # slot 34   category 3
    "boltgrabber",                 # slot 35   category 3
    "boxbreaker",                  # slot 36   category 3
    "superkick",                   # slot 37   category 3
    "kickblast",                   # slot 38   category 3
    "kicksplosion",                # slot 39   category 3
]

# Named slot ids, e.g. WeaponSlot.SHOCKROCKET == 5.
WeaponSlot = IntEnum(
    "WeaponSlot", {name.upper(): index for index, name in enumerate(WEAPON_ORDER) if name is not None},
)

"""Equipment display names, their native WEAPON_ORDER names, and the case each is found in."""
from dataclasses import dataclass

from .clank_gadgets import SACClankGadgets, SACClankWeapons
from .planets import SACCases
from .weapon_order import WEAPON_ORDER, WeaponSlot


@dataclass(frozen=True)
class SACRatchetWeapons:
    SHOCKROCKET       = "Shock Rocket (Ratchet)"
    PLASMAWHIP        = "Plasma Whip (Ratchet)"
    PORKBOMB          = "Pork Bomb Gun (Ratchet)"
    KICKBLAST         = "Clank Fu Hot Foot (Clank)"  # Legacy attribute/order preserves item IDs.
    BLASTER           = "Dual Lacerators (Ratchet)"
    SHARDGUN          = "Shard Gun (Ratchet)"
    BEEMINEGLOVE      = "Bee Mine Mk. II (Ratchet)"
    WALLOPER          = "Walloper (Ratchet)"
    MINELAUNCHER      = "Mine Launcher (Ratchet)"
    RATCHETPDA        = "Gadgetron PDA (Ratchet)"
    BOLTTRANSFER      = "Bolt Extractor (Ratchet)"
    RYNO              = "RYNO (Ratchet)"


@dataclass(frozen=True)
class SACProgressiveRatchetWeapons:
    SHOCKROCKET       = "Progressive Shock Rocket (Ratchet)"
    PLASMAWHIP        = "Progressive Plasma Whip (Ratchet)"
    PORKBOMB          = "Progressive Pork Bomb Gun (Ratchet)"
    BLASTER           = "Progressive Dual Lacerators (Ratchet)"
    SHARDGUN          = "Progressive Shard Gun (Ratchet)"
    BEEMINEGLOVE      = "Progressive Bee Mine Mk. II (Ratchet)"
    WALLOPER          = "Progressive Walloper (Ratchet)"
    MINELAUNCHER      = "Progressive Mine Launcher (Ratchet)"
    RATCHETPDA        = "Progressive Agency PDA (Ratchet)"
    BOLTTRANSFER      = "Progressive Bolt Transfer (Ratchet)"
    RYNO              = "Progressive RYNO (Ratchet)"


@dataclass(frozen=True)
class SACTitanWeapons:
    """Fully-upgraded (NG+ Titan Vendor) counterpart to SACRatchetWeapons -- only the
    weapons with a Titan tier get a member here, matched by shared attribute name to
    the SACRatchetWeapons entry it upgrades (see constants/weapon_progression.py)."""
    SHOCKROCKET  = "Titan Shock Rocket (Ratchet)"
    PLASMAWHIP   = "Titan Plasma Whip (Ratchet)"
    PORKBOMB     = "Titan Pork Bomb Gun (Ratchet)"
    BLASTER      = "Titan Dual Lacerators (Ratchet)"
    SHARDGUN     = "Titan Shard Gun (Ratchet)"
    BEEMINEGLOVE = "Titan Bee Mine Mk. II (Ratchet)"
    WALLOPER     = "Titan Walloper (Ratchet)"
    MINELAUNCHER = "Titan Mine Launcher (Ratchet)"


@dataclass(frozen=True)
class SACQwarkWeapons:
    """Qwark's weapons. Not randomized; listed for reference only."""
    QWARKBLASTER      = "Blaster (Qwark)"
    GIANTQWARKBLASTER = "Giant Blaster (Qwark)"


# Category order is also the historical AP item allocation order.
RATCHET_WEAPONS: tuple[str, ...] = (
    SACRatchetWeapons.SHOCKROCKET,
    SACRatchetWeapons.PLASMAWHIP,
    SACRatchetWeapons.PORKBOMB,
    SACRatchetWeapons.KICKBLAST,
    SACRatchetWeapons.BLASTER,
    SACRatchetWeapons.SHARDGUN,
    SACRatchetWeapons.BEEMINEGLOVE,
    SACRatchetWeapons.WALLOPER,
    SACRatchetWeapons.MINELAUNCHER,
    SACRatchetWeapons.RATCHETPDA,
    SACRatchetWeapons.BOLTTRANSFER,
    SACRatchetWeapons.RYNO,
)
GADGETS_FROM_WEAPON_TABLE: tuple[str, ...] = (
    SACClankGadgets.CLANKPDA,
    SACClankGadgets.JETBOOTS,
    SACClankGadgets.OMNIKEY,
    SACClankGadgets.HYPNOWATCH,
    SACClankGadgets.HOLOMONOCLE,
    SACClankGadgets.BOLTGRABBER,
    SACClankWeapons.THROWTIE,
    SACClankWeapons.CUFFLINK,
    SACClankWeapons.TANGLEVINE,
    SACClankWeapons.FLAMETHROWERPEN,
    SACClankWeapons.HOLOKNUCKLES,
    SACClankWeapons.SUPERKICK,
    SACClankWeapons.LIGHTNINGUMBRELLA,
    SACClankWeapons.KICKSPLOSION,
)

# One shared native equipment lookup, with its reverse for runtime checks.
# Attribute names match WeaponSlot, so no parallel hand-maintained slot map
# is needed. The positional pen/shades pickups remain separate below.
EQUIPMENT_DISPLAY_TO_INTERNAL: dict[str, str] = {
    display: WEAPON_ORDER[WeaponSlot[attr]]
    for cls in (SACRatchetWeapons, SACClankGadgets, SACClankWeapons)
    for attr, display in vars(cls).items()
    if display in (*RATCHET_WEAPONS, *GADGETS_FROM_WEAPON_TABLE)
}
EQUIPMENT_INTERNAL_TO_DISPLAY = {
    internal: display for display, internal in EQUIPMENT_DISPLAY_TO_INTERNAL.items()
}
CLANK_PICKUP_TO_INTERNAL = {
    SACClankGadgets.BLACK_OUT_PEN: "fountainpen",
    SACClankGadgets.THERM_OPTIC_SHADES: "sunglasses",
}


# Case -> the Ratchet weapons found there.
# LOW CONFIDENCE: entries may move once each case is verified in-game.
WEAPONS_BY_CASE: dict[str, tuple[str, ...]] = {
    SACCases.BOLTAIRE_MUSEUM: (
        SACRatchetWeapons.BLASTER,
    ),
    SACCases.MAX_SECURITY_CELLS: (
        SACRatchetWeapons.SHARDGUN, SACRatchetWeapons.WALLOPER,
    ),
    SACCases.ASYANICA_ROOFTOPS: (
        SACRatchetWeapons.MINELAUNCHER,
    ),
    SACCases.AZCOTAL_ALLEY: (
        SACRatchetWeapons.BEEMINEGLOVE,
    ),
    SACCases.HIGH_ROLLERS_CASINO: (
        SACRatchetWeapons.PORKBOMB,
    ),
    SACCases.VENANTONIO_LABS: (
        SACRatchetWeapons.PLASMAWHIP, SACRatchetWeapons.KICKBLAST,
    ),
    SACCases.GALACTIC_BOLT_RESERVE: (
        SACRatchetWeapons.SHOCKROCKET,
    ),
    SACCases.KLUNKS_LAIR: (
        SACRatchetWeapons.RYNO,
    ),
}

# Case -> the Clank equipment from the WEAPON_ORDER array found there.
# LOW CONFIDENCE, like WEAPONS_BY_CASE.
GADGETS_BY_CASE: dict[str, tuple[str, ...]] = {
    SACCases.BOLTAIRE_MUSEUM: (
        SACClankWeapons.THROWTIE, SACClankGadgets.JETBOOTS,
        SACClankWeapons.HOLOKNUCKLES, SACClankWeapons.SUPERKICK,
        SACClankGadgets.BLACK_OUT_PEN, SACClankGadgets.THERM_OPTIC_SHADES,
    ),
    SACCases.ASYANICA_ROOFTOPS: (
        SACClankWeapons.CUFFLINK, SACClankGadgets.OMNIKEY,
    ),
    SACCases.AZCOTAL_ALLEY: (
        SACClankWeapons.TANGLEVINE, SACClankGadgets.CLANKPDA,
    ),
    SACCases.HIGH_ROLLERS_CASINO: (
        SACClankGadgets.HYPNOWATCH, SACClankGadgets.HOLOMONOCLE,
    ),
    SACCases.VENANTONIO_LABS: (
        SACClankWeapons.FLAMETHROWERPEN, SACClankWeapons.LIGHTNINGUMBRELLA,
    ),
    SACCases.GALACTIC_BOLT_RESERVE: (
        SACClankGadgets.BOLTGRABBER,
    ),
    SACCases.KLUNKS_LAIR: (
        SACClankWeapons.KICKSPLOSION,
    ),
}

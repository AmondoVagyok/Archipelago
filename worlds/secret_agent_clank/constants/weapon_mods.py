"""Native mod IDs, GadgetData slots and English labels from the USA mod catalog."""
from typing import NamedTuple


class WeaponMod(NamedTuple):
    mod_id: int
    weapon: str
    slot: int
    name: str
    ng_plus: bool = False

    @property
    def location(self):
        return f'Mod Vendor: {self.name}'


WEAPON_MODS = (
    WeaponMod(1, 'blaster', 0, 'Seeker Mod (Lacerators)'),
    WeaponMod(2, 'blaster', 1, 'Hunter Mod (Lacerators)'),
    WeaponMod(4, 'shardgun', 0, 'Icy Halo Mod (Shard Gun)'),
    WeaponMod(5, 'shardgun', 1, 'Charge-Up Mod (Shard Gun)'),
    WeaponMod(7, 'beemineglove', 0, 'Explosive Nature Mod (Bee Mine)'),
    WeaponMod(8, 'beemineglove', 1, 'Killer Honey Mod (Bee Mine)'),
    WeaponMod(10, 'shockrocket', 0, 'Static Charge Mod (Shock Rocket)'),
    WeaponMod(11, 'shockrocket', 1, 'Taser Mod (Shock Rocket)'),
    WeaponMod(13, 'walloper', 0, 'Lightning Speed Mod (Walloper)'),
    WeaponMod(14, 'walloper', 1, 'Earthquake Mod (Walloper)'),
    WeaponMod(16, 'plasmawhip', 0, 'Flame Trails Mod (Plasma Whip)'),
    WeaponMod(17, 'plasmawhip', 1, 'Fire Snake Mod (Plasma Whip)'),
    WeaponMod(19, 'porkbomb', 0, 'War Pigs Mod (Pork Bomb)'),
    WeaponMod(20, 'porkbomb', 1, 'Tasty Pigs Mod (Pork Bomb)'),
    WeaponMod(22, 'minelauncher', 0, 'Ordnance Mod (Mine Launcher)'),
    WeaponMod(23, 'minelauncher', 1, 'Persistence Mod (Mine Launcher)'),
    WeaponMod(25, 'FlamethrowerPen', 0, 'Molten Bolt Mod (Flamethrower)', True),
    WeaponMod(28, 'LightningUmbrella', 0, "Xeno's Capacitor Mod (Umbrella)", True),
    WeaponMod(29, 'LightningUmbrella', 1, 'Thundercloud Mod (Umbrella)', True),
)


def enabled_mods(characters, ng_plus):
    return tuple(mod for mod in WEAPON_MODS
                 if ('Clank' if mod.ng_plus else 'Ratchet') in characters
                 and (not mod.ng_plus or ng_plus > 0))

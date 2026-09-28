# Equipment location source audit

Checked against the Secret Agent Clank wiki on 28 September 2026. This audits
equipment acquisition sources; it does not establish native hook correctness.

## Vendor purchases

The [vendor catalog](https://ratchetandclank.fandom.com/wiki/Secret_Agent_Clank_vendors)
identifies one Agency vendor with the following purchases:

| Equipment | Classification |
| --- | --- |
| Holo Knuckles, Thunderstorm Umbrella, HypnoWatch | Clank vendor |
| Agency PDA, Bolt Grabber | Clank vendor |
| Clank Fu Kick, Clank Fu Hot Foot | Clank vendor |
| Hot Foot 2.1 Beta | Clank vendor, NG+ |
| Pork Bomb Gun, Plasma Whip, Shock Rocket | Ratchet vendor |
| RYNO | Ratchet vendor, NG+ |
| Titan/Proto weapon upgrades | Same vendor, NG+ |
| 14 Ratchet weapon mods, three NG+ Clank mods | Same vendor |

The Shard Gun Charge-Up mod (No Shelter) and Walloper Earthquake mod (Past Due)
are challenge rewards. They are excluded from the vendor purchase catalog.

## Pickups and other rewards

| Equipment | Source | Evidence |
| --- | --- | --- |
| Tie-A-Rang, Blackout Pen, Dual Lacerators, Jet Boots | Museum pickups | [Boltaire Museum](https://ratchetandclank.fandom.com/wiki/Boltaire_Museum) |
| Cufflink Bomb, Mine Launcher | Clank's Asyanica Rooftops pickups | [Number Woo works for...?](https://ratchetandclank.fandom.com/wiki/Number_Woo_works_for...%3F) |
| Omni-Key 5000 | Asyanica Rooftops pickup | [Omni-Key 5000](https://ratchetandclank.fandom.com/wiki/Omni-Key_5000) |
| Holo-Monocle | Casino Paradise Exploited, free acquisition | [Holo-Monocle](https://ratchetandclank.fandom.com/wiki/Holo-Monocle) |
| Blowtorch Briefcase | Crashing the Party pickup | [Crashing the Party](https://ratchetandclank.fandom.com/wiki/Crashing_the_Party) |
| Shard Gun | Prison floor, Karmic Beatdown | [Shard Gun](https://ratchetandclank.fandom.com/wiki/Shard_Gun) |
| Walloper | Free in Karmic Beatdown | [Vendor catalog](https://ratchetandclank.fandom.com/wiki/Secret_Agent_Clank_vendors) |
| Tanglevine Carnation, Bee Mine Mk. II | Free on Rionosis | [Vendor catalog](https://ratchetandclank.fandom.com/wiki/Secret_Agent_Clank_vendors) |
| Therm-Optic Shades | Escape the Ravine pickup, native NG+ | [Therm-Optic Shades](https://ratchetandclank.fandom.com/wiki/Therm-Optic_Shades) |
| Bolt Extractor | Nails for Breakfast challenge reward | [Slim Cognito's Bolt Extractor](https://ratchetandclank.fandom.com/wiki/Slim_Cognito%27s_Bolt_Extractor) |
| Gadgetron PDA | No good deed goes unpunished challenge reward | [Gadgetron Personal Delivery Assistant](https://ratchetandclank.fandom.com/wiki/Gadgetron_Personal_Delivery_Assistant) |

Bolt Extractor is represented by its challenge, not a vendor purchase. The
Ratchet PDA is named Gadgetron PDA; Agency PDA belongs to Clank. Legacy internal
equipment slot names remain unchanged to preserve item IDs.

The nonexistent Asyanica Rooftops and Spaceship Graveyard enter-cutscene checks
were removed as reported. Numeric location IDs were not reassigned. Regenerate
seeds for the corrected catalog and equipment names; restart the client and
reset/change levels to install the updated native hooks.

The AP vendor intentionally ignores native purchase availability. Enabled
characters and NG+ seed options still determine which purchase checks exist.
The wiki's native progression descriptions are not additional vendor gates.

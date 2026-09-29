# Skill point checks

Set `skill_points` in your Secret Agent Clank YAML:

```yaml
skill_points: easy  # off, easy, or hard
```

- `off`: no skill point checks (default).
- `easy`: 27 easier checks before operative filtering.
- `hard`: all 65 checks, including the 38 harder checks.

Legacy `true` means `hard`; `false` means `off`. Numeric values are 0, 1, and 2.
Removing an operative from `operatives`, or setting it to `0`, removes its skill
point checks. Special Missions is an independent option group, including vehicle,
rhythm, and Giant Clank missions; these do not additionally require the Clank group.

The [Ratchet & Clank Wiki skill point guide](https://ratchetandclank.fandom.com/wiki/Secret_Agent_Clank_skill_points)
provides the objectives and mission associations. Difficulty is a project judgment,
not an official wiki rating: easy favors repeatable actions and forgiving weapon
restrictions; hard includes flawless runs, exhaustive objectives, strict timers,
precision scores, and long or inconsistent challenges. These are initial tiers,
not a claim that every player will find each challenge equally difficult.

Two ownership details matter:

- A Gadgebot Stands Alone occurs inside the casino Special Mission and requires
  both Special Missions and Gadgetbots to be enabled.
- Vault Vault is earned in the Gadgetbots' Vaultbreakers challenge. Its AP region
  is Inside the A-Eye. Its existing AP name, numeric ID and native memory flag
  remain unchanged, even though the legacy name mentions Galactic Bolt Reserve.

The table uses the existing in-project titles, including legacy spellings.
Each row names its gameplay case and all required option groups. Existing gameplay
item rules are unchanged except Vault Vault now inherits its Gadgetbot case access
instead of the reserve's Clank gadget requirement. These changes are tested at
world generation; they have not been verified in a live emulator session.

| Skill point | Tier | Required operatives | Gameplay case |
| --- | --- | --- | --- |
| Furious Fists of Fury | easy | Clank | Boltaire Museum |
| Silent Night | hard | Clank | Boltaire Museum |
| Pyrrhic Victory | hard | Special Missions | Boltaire Gem Wing |
| Triple Platinum Record | hard | Special Missions | Boltaire Gem Wing |
| Stainless Steel | hard | Ratchet | Max-Security Cells |
| Playing With Fire | easy | Ratchet | Max-Security Cells |
| Speed Demon | hard | Gadgetbots | Rooftop Deathtrap |
| Perfect Chrome Finish | hard | Gadgetbots | Rooftop Deathtrap |
| Robot Finds Ninja | hard | Clank | Asyanica Rooftops |
| Black Tie Affair | easy | Clank | Asyanica Rooftops |
| Like The Wind | hard | Clank | Asyanica Rooftops |
| Inverse Ninja Law | easy | Qwark | Larger Than Life |
| Blaster Overload | easy | Qwark | Larger Than Life |
| Perfect Tango | hard | Special Missions | Countess's Villa |
| Black Diamond | hard | Special Missions | Glaciara, Ski Slopes |
| Smooth Moves | easy | Special Missions | Glaciara, Ski Slopes |
| Ringleader | hard | Special Missions | Glaciara, Ski Slopes |
| Empty The Warrens | hard | Ratchet | The Mess Hall |
| Antaeus | hard | Ratchet | The Mess Hall |
| Master of Disguise | hard | Clank | Azcotal Alley |
| Trash Talk | hard | Clank | Azcotal Alley |
| Deadly Hands | hard | Clank | Azcotal Alley |
| Steel Rain | easy | Clank | Gondola Ascent |
| 52 Card Pickup | easy | Qwark | Suck and Jive |
| Dress For Success | easy | Qwark | Suck and Jive |
| Beat The House | hard | Clank | High-Rollers Casino |
| Indian Burn | easy | Ratchet | The Exercise Yard |
| The Law Can't Touch Me | hard | Ratchet | The Exercise Yard |
| Lucky Sevens | hard | Special Missions | High Stakes Room |
| A Gadgebot Stands Alone | hard | Gadgetbots, Special Missions | High Stakes Room |
| All Slime Must Burn | easy | Clank | Venantonio Labs |
| Ramming Speed! | easy | Clank | Venantonio Labs |
| Evasive Maneuvers | easy | Special Missions | Venantonio Canals |
| Deep Six | hard | Special Missions | Venantonio Canals |
| Wake Of Destruction | hard | Special Missions | Venantonio Canals |
| Ringmaster | hard | Special Missions | Venantonio Canals |
| Twinkle Toes | hard | Qwark | Madam Butterqwark |
| Magnum Opus | hard | Qwark | Madam Butterqwark |
| Sold Out | hard | Qwark | Madam Butterqwark |
| With Interest | easy | Clank | Galactic Bolt Reserve |
| Androids In Disguise | easy | Clank | Galactic Bolt Reserve |
| Vault Vault | hard | Gadgetbots | Inside the A-Eye |
| El Día de los Muertos | easy | Gadgetbots | Inside the A-Eye |
| Ruba-Dub Club | easy | Ratchet | The Showers |
| Modesty | hard | Ratchet | The Showers |
| It's A Delicacy Somewhere | hard | Clank | Spaceship Graveyard |
| Revenant | hard | Clank | Spaceship Graveyard |
| Punchy | easy | Qwark | Saint Qwark |
| Sour Victory | easy | Qwark | Saint Qwark |
| Min Maxing | hard | Special Missions | The Quasar Fields |
| I Kill the Rock | easy | Special Missions | The Quasar Fields |
| Whip It Good | easy | Ratchet | Prison Breakout! |
| Hanging Judge | hard | Ratchet | Prison Breakout! |
| Yeeee Haaaaaw! | easy | Special Missions | Dam's Edge, Hydrano |
| Offensive Driver | hard | Special Missions | Dam's Edge, Hydrano |
| Slippery Slope | easy | Special Missions | Dam's Edge, Hydrano |
| Ring Around the Rosie | hard | Special Missions | Dam's Edge, Hydrano |
| He Cleans pools, Too! | easy | Qwark | A Fiction Full Of Dollars |
| Perfect Mirror | hard | Qwark | A Fiction Full Of Dollars |
| Cerial Decoder Rung | hard | Gadgetbots | Bulkhead Lock |
| I33t h4XX0r | hard | Clank | Underwater Bunker |
| Rust Proof | easy | Clank | Underwater Bunker |
| I'm not There | hard | Clank | Underwater Bunker |
| Turn The Tables | easy | Clank | Klunk's Lair |
| A Pretty Good Likeness | easy | Clank | Klunk's Lair |

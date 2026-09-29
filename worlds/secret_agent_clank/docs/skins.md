# Skins

AP unlocks all 21 menu skins, plus Qwark's four matching giant forms, when
the connection initializes gameplay. No Titanium Bolts are spent, and no
story, challenge-mode, or location-check flags are granted.

Choose `clank_skin`, `ratchet_skin`, and `qwark_skin` under **SAC Cosmetics**
in your player YAML. Each defaults to `in_game`, which keeps your selection
in the game's Special → Skins menu. Choosing a specific skin supplies an initial
default when AP first unlocks skins for the save. Later menu selections persist
through polling, level loads, and reconnects. Saves with all skins already
unlocked retain their current selections.

```yaml
Secret Agent Clank:
  clank_skin: zoni
  ratchet_skin: kung_fu_ratchet
  qwark_skin: lucha_libre_qwark
```

Connect before loading a level. If connecting while already playing, use the
client's usual in-game level reset to initialize AP and apply the selected skin.
The game retains its native restrictions for special sequences and minigames.

| Character | Choices (besides `in_game`) |
| --- | --- |
| Clank | `suit`, `cowboy`, `klunk`, `70s_clank`, `cop_clank`, `blender`, `zoni` |
| Ratchet | `prison_scrubs`, `towel`, `super_incognito`, `tropical_vacation`, `plundering_pirate_captain`, `ratchetzilla`, `robo_ratchet`, `kung_fu_ratchet`, `zombie_ratchet`, `dan` |
| Qwark | `regular`, `cowboy`, `maid_qwark`, `lucha_libre_qwark` |

## Native layout evidence

Verified on the USA PS2 (`SCUS-97623`) captures in `.research`: the skin menu
contains 10 Ratchet entries (IDs 1–10), 7 Clank entries (11–17), and 4 Qwark
entries (18–21). The localized menu strings supply the option names. Qwark's
normal-to-giant conversion maps IDs 18–21 to 22–25.

`SelectedSPHeroSkinID__F8PLR_TYPE` reads a signed byte at save + `0x19900`
+ player type × `0x34` (Ratchet 0, Clank 1, Qwark 2, giant Qwark 3).
`SCRNSKINSCREEN_Update__Fv` tests and sets owned skin bits at save + `0x199D4`.
The save pointer is resolved from validated `GLOBAL_GetFlag__FUiUc` code.

`IsSkinUnlocked__F12SPHeroSkinId` controls menu visibility separately from
ownership; AP replaces its result with true rather than changing prerequisite
story flags. Its unreachable body holds initialization code reached from
`HEROSKIN_LoadSelectedSpecilaSkin__Fv`, just before the original selected-skin
read and model swap. This also covers a fresh save initialized after the loader
gate. Both edits belong to the existing loader patch journal and are validated
and restored with the other hooks. Host sync preserves unrelated ownership bits
and follows save-pointer relocation.

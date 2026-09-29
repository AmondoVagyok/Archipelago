# Clank nanotech checks

The USA PS2 capture `.research/vendor_audit_live.ram` establishes:

- `g_LevelProgressionExperienceData_Clank` (capture address 0x5A5850)
  contains 71 records of (zero-based level, cumulative XP, maximum health).
  It starts at (0, 0, 15) and ends at (70, 469200, 85).
- `GLOBALVARS_GetPlayerMaxLevel__FP6PLAYER` (0x35F610) selects the
  Clank count table at 0x5E5768: 46 entries in NG, 71 in NG+.
  These counts include the starting level, giving health caps of 60 and 85.
  NG+ values 1 and 2 both select the second count.
- `GLOBALVARS_AddClankExperience__Fi` (0x361060) reads Clank XP at
  pGV + 0x19930. The general XP routine uses pGV + 0x198FC + operative*0x34;
  Ratchet is operative 0 and Clank is operative 1. This is saved XP, not
  current health, the HUD, or the currently active player's level.

Runtime resolves relocated exports, verifies the Clank table and save layout,
then reads Clank XP after save initialization. All earned checks are retried
through the existing checked-location delivery path, including after reconnect.
NG generation includes levels 16-60; both NG+ options include 16-85. Checks
require an accessible Clank case, and are absent when Clank is disabled.

`nanotech_checks` defaults on for new seeds. Old slot data defaults off.
The existing `health_xp_multiplier` YAML/slot key remains compatible and its
UI label is now Nanotech XP Multiplier; it scales native health XP gains.
`weapon_xp_multiplier` already supports 1-10 and is inactive in automatic
Progressive Weapons mode. Neither multiplier needed a duplicate option.

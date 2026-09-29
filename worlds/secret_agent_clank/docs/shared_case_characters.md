# Shared-module character selection (SCUS-97623)

## Gondola Ascent and Suck and Jive

Both cases load native module **11**. The loaded module number alone cannot
identify the selected case or player character.

The native selector is global flag **0xC8**:

- `0`: Clank / Gondola Ascent.
- `1`: Qwark / Suck and Jive.

`GLOBAL_GetFlag__FUiUc` reads flags at `save_pointer + 0x4E0 + index`.
Consequently the selector is at **save_pointer + 0x5A8**, or **0x206CA8**
when the save pointer is `0x206700` as in the September 29, 2026 live captures.
Resolve the save pointer through `GlobalFlags.bind()` rather than assuming
that its pointer-storage address is identical across loaded modules.

The native mission records distinguish these cases independently of the
currently highlighted Operatives menu row:

| Case | Module (+0x30) | Operative mask (+0x34) | Parent label (+0x38) | Case label (+0x3C) |
| --- | --- | --- | --- | --- |
| Gondola Ascent | 11 | 2 | 5602 | 5614 |
| Suck and Jive | 11 | 8 | 5603 | 5622 |

`SCRNGALACTICMAP_Update__Fv` compares the selected mission's module and
operative mask, sets flag 0xC8, then requests the transition. It also sets
global flag 0xCA (save +0x5AA), which marks a manual case entry.
`IsSameLevel__FP8tMISSIONP15tPAUSEMENU_NODE` checks flag 0xC8 when deciding
whether a selection in the shared module can simply resume gameplay.
`Level04GondolaSegmentController_FixLinks__FP4Moby` reads flag 0xC8 to choose
the entry checkpoint and calls `Lvl04GondolaChaseCtrl_SetQwarkSegment__Fv`
for the Qwark entry.

The existing `StartingCase` wrappers set this selector for new-save starts.
Do not force it to 1 for every module-11 load: that would break Gondola Ascent.
Do not rewrite it based on a highlighted menu row while browsing Case Files.

## Live investigation, September 29, 2026

Suck and Jive's native mission was unlocked by changing its state at +0x0C
from 1 to 2. Entering it through Case Files loaded module 11 with flag 0xC8
equal to 1, and the user confirmed Qwark appeared.

In that capture:

- `GLOBAL_GetFlag__FUiUc`: `0x35E700`.
- Save-pointer storage derived from that getter: `0x594BB0`.
- Save pointer: `0x206700`.
- `g_pActivePlayer`: `0x5BF990`, pointing to `0x183BA14`.
- Active player's vtable at player +0x574: `0x5EF748`.
- Player type at vtable +0x44: **2 (Qwark)**.
- `g_pClankPlayer` also pointed to a valid Clank object (type **1**).
  Its presence is not evidence that Clank is the active character.

The reported incorrect-character state could not be reproduced during this
investigation. No runtime character patch was applied. The local research
captures and extracted module are ignored under `.research/`.

If the problem recurs, capture the active player type, 0xC8, entry checkpoint,
selected mission record, and transition route before changing memory. A
module number or the presence of a Clank object alone is insufficient to
diagnose this issue.

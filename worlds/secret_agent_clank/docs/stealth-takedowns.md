# Stealth takedown checks

```yaml
stealth_takedown_checks: off  # off, every_5, every_10, all
```

- `off` (default): no checks.
- `every_5`: 5, 10, 15, 20, 25 takedowns.
- `every_10`: 10 and 20 takedowns.
- `all`: one check at each total from 1 through 25.

Enabling this option without Clank in `operatives` raises `OptionError` during
`generate_early`. Older slot data defaults off. These are cumulative successful
takedowns, not 25 individually identified enemies. Repeat takedowns count.

## Access rules still to map

Edit `rules/stealth.py`, which has explicit TODOs at:

- `stealth_5_rule`: totals 1-5.
- `stealth_10_rule`: totals 6-10, in addition to the first rule.
- `stealth_25_rule`: totals 11-25, in addition to both earlier rules.

The exact cases and equipment requirements are not established yet. Until those
TODOs are filled in, the conservative placeholder requires all enabled Clank case
regions. It does not claim every Clank case contains takedowns. Replace each
function with the actual `CanReachRegion` / `Has` rule when the routes are known.
This placeholder is not a verified item-access route for 25 takedowns.

## PS2 evidence and implementation

The supplied PS4 Lua screenshot increments its own `StealthStorageAddr` byte and
saves it in emulator configuration. It does not establish a PS2 lifetime counter.
The native `CLANKSTEALTH_GiveStealthKill__FP4Mobyf` list count is unsuitable:
`CLANKSTEALTH_UseStealthMultiplier__FiPC4Moby` removes entries and decrements it.

In the local `suck_and_jive_live.ram` capture, `End__15StealthTakeDown` is at
0x457940. Two failure-state bytes at transient-data offsets 0x15 and 0x2C select
alternate handling. The successful path calls `CLANKSTEALTH_GiveStealthKill`
at End + 0xB0 (0x4579F0 in that capture). Runtime resolves exports each module,
checks the branch/call signatures, and redirects only that success call.
The original delay slot, moby argument, floating-point argument, return address,
and native reward call are preserved. This counts Clank's takedown state only,
not generic enemy kills or the stealth bonus multiplier.

The AP counter is a saturating 0-25 word allocated in verified hook storage.
Its address varies by module and options; `Core.stealth.binding[0]` is the bound
address. Installation is limited to modules containing Clank cases. Shared
modules still intercept only Clank's takedown function.

The client polls before servicing the loader and carries the observed total
between modules. Server data storage `secret_agent_clank_stealth_<team>_<slot>`
uses a monotonic maximum and is loaded before allowing a new hooked level to
start. Old pending milestones retry through the normal location delivery path.
Savestate rollback cannot lower the total already observed by this client.

Keep the AP client connected while playing. This is not a new native save-game
field: unobserved events can be lost if the module is replaced or the emulator
exits before the client polls, and unsent progress can be lost if the client
process exits before persistence. Offline play and arbitrary savestate replay
are not guaranteed. A live gameplay check of successful versus failed takedowns,
level changes, and reconnects remains necessary; current verification uses RAM
captures, an instruction interpreter, and generation tests.

Combined pickup/vendor/progression/stealth plans are exercised on the available
Clank captures. Two existing capture limitations remain outside this change:
`ConnectionWarning` expects a different HUD prologue, and the module 11 manual
weapon-progression plan exhausts hook storage even without stealth. The combined
test omits the warning hook and explicitly skips that manual-progression case.

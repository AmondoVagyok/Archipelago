"""Every module here reads original native instruction bytes, builds
REPLACEMENT machine code, and writes it into the game's code region to
change control flow -- as opposed to core/'s other files, which only
read/write plain data fields (flags, counts, HUD text) and never construct
new instructions. If a module doesn't build/install a Patch, it doesn't
belong in this package -- see mips.py's docstring for the mnemonic layer
used to write new routines by hand.

- asm.py: shared MIPS/patch-plan primitives (words/packed/jump/branch/Patch).
- mips.py: named-mnemonic instruction encoders for hand-written routines.
- flag_routines.py: the native routine generators the location-hook plans patch in.
- locations.py: VENDOR_LOCATIONS/PICKUP_LOCATIONS, the AP location tables.
- plan.py: PatchPlan, the shape both location-hook plan builders return.
- weapon_pickup.py / vendor_only.py: the two location-hook patch plans.
- hooks.py: LocationHooks, the runtime-facing class tying those two together.
- loader_gate.py: LoaderGate, holds/releases the resident level-load thread
  by patching one branch instruction.
- wrench.py: WrenchProgression, gates Ratchet's wrench input by masking
  ANDI immediates in 3 native control routines.
- gain_storage.py: prepare_gain_storage(), frees code space shared by the
  weapon-mod and progression patches below.
- mission_travel.py: prepare_mission_travel(), repoints case-transition calls.
- progression.py: Progression, the weapon/health XP multiplier patch.
- starting_case.py: StartingCase, the new-save case-override patch.
- titan_vendor.py: prepare_titan_vendor()/prepare_titan_price()/
  prepare_disable_titan_offers(), the NG+ Titan weapon vendor patches.
- weapon_mods.py: WeaponMods, the native weapon-mod vendor patch.

Re-exported here so callers can keep importing from `.patches` rather than
reaching into the individual submodules -- new additions above generally
import their own submodule directly instead (see core/core.py) rather than
growing this list further."""
from .asm import MARKER, Patch, branch, jump, packed, words
from .flag_routines import entitlement_routine, flag_routine
from .hooks import LocationHooks
from .locations import PICKUP_LOCATIONS, VENDOR_LOCATIONS
from .plan import PatchPlan

__all__ = [
    "MARKER", "PICKUP_LOCATIONS", "Patch", "PatchPlan", "VENDOR_LOCATIONS",
    "LocationHooks", "branch", "entitlement_routine", "flag_routine", "jump", "packed", "words",
]

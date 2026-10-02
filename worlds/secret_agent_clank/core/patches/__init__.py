"""Native code patches: each module verifies the original instructions and writes replacement machine code."""
from .asm import MARKER, Patch, branch, jump, packed, words
from .entitlements import Entitlements
from .gameFlags import GameFlags
from .hooks import LocationHooks
from .locations import PICKUP_LOCATIONS, VENDOR_LOCATIONS
from .plan import PatchPlan

__all__ = [
    "MARKER",
    "PICKUP_LOCATIONS",
    "VENDOR_LOCATIONS",
    "Entitlements",
    "GameFlags",
    "LocationHooks",
    "Patch",
    "PatchPlan",
    "branch",
    "jump",
    "packed",
    "words",
]

"""Native code patches: each module verifies the original instructions and writes replacement machine code."""
from .asm import MARKER, Patch, branch, jump, packed, words
from .connection_warning import HEARTBEAT_FRAMES, ConnectionWarning
from .entitlements import Entitlements
from .gain_storage import GainStorage
from .gameFlags import GameFlags
from .hooks import LocationHooks
from .keycard_hunt import KeycardHunt
from .loader_gate import LoaderBarrierLost, LoaderGate
from .mission_travel import MissionTravel
from .patch import PatchSet
from .plan import PatchPlan
from .progression import Progression
from .starting_case import StartingCase
from .storage import free_blocks, plan_storage, storage_address
from .titan_vendor import TitanOffers, TitanPrice, TitanVendor
from .vendor_catalog import VendorCatalog
from .vendor_icon_preview import VendorIconPreview
from .vendor_offer_preview import VendorOfferPreview
from .vendor_presentation import VendorPresentation
from .vendor_tabs import VendorTabs
from .vendor_text_preview import VendorTextPreview
from .weapon_mods import WeaponMods
from .wrench import PROGRESSIVE_WRENCH, WrenchProgression

__all__ = [
    "HEARTBEAT_FRAMES",
    "MARKER",
    "PROGRESSIVE_WRENCH",
    "ConnectionWarning",
    "Entitlements",
    "GainStorage",
    "GameFlags",
    "KeycardHunt",
    "LoaderBarrierLost",
    "LoaderGate",
    "LocationHooks",
    "MissionTravel",
    "Patch",
    "PatchPlan",
    "PatchSet",
    "Progression",
    "StartingCase",
    "TitanOffers",
    "TitanPrice",
    "TitanVendor",
    "VendorCatalog",
    "VendorIconPreview",
    "VendorOfferPreview",
    "VendorPresentation",
    "VendorTabs",
    "VendorTextPreview",
    "WeaponMods",
    "WrenchProgression",
    "branch",
    "free_blocks",
    "jump",
    "packed",
    "plan_storage",
    "storage_address",
    "words",
]

"""No Glaciara Ski Slopes-specific items yet -- see
items/__init__.py's ALL_ITEMS for what's actually in the pool today
(built from flat category tables, not per-case). This file is a
placeholder extension point, same "declared ahead of its data" empty-stub
pattern as rules/glaciara_ski_slopes.py -- add case-specific item entries here once
needed."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SACItemData

GLACIARA_SKI_SLOPES_ITEMS: dict[str, "SACItemData"] = {}

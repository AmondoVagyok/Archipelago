"""Per-check-category native state trackers -- one *Inventory class each,
reading/writing PINE memory to detect and confirm AP checks:

- inventory.py: ItemInventory, the base per-item ownership tracker.
- weapons.py: WeaponInventory (Ratchet weapons/Clank WEAPON_ORDER gadgets).
- planets.py: CaseInventory (which case is currently loaded/owned).
- case_struct.py: CaseStructInventory (the case-unlock table).
- case_unlocks.py: CaseUnlockInventory (+ resolve_owned_cases()).
- case_events.py: CaseEventInventory, the shared bitflag-event base class
  for cutscenes.py/gadgetbot_challenges.py/ratchet_challenges.py/
  special_challenges.py (and core/skill_points.py, which stays in core/).
- missions.py: MissionInventory (CHAPTER_ENTRIES-based story missions).
- alien_codes.py / keycards.py: their own collectible-flag trackers."""

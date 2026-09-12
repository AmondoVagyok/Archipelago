"""Shared, dependency-free building blocks for the per-case location files
in this package -- kept in their own leaf module (no imports from `.` or
from any case file) so every locations/<case>.py file can import them at
module load time with no circular-import ordering concerns. The
constants.missions import below is fine despite that -- constants/ never
imports back from locations/, so it doesn't create a cycle."""
from typing import Callable, NamedTuple

from ..constants.missions import CHAPTER_ENTRIES

BASE_ID = 77_800_000

# Generous per-case id block -- no case comes close to needing 1000 distinct
# location ids, this just gives every case file a fixed, non-overlapping id
# range it can compute on its own (BASE_ID + (case_id - 1) * this), instead
# of sharing one mutable counter across all 30 files (which would force a
# strict import order between them).
CASE_ID_BLOCK_SIZE = 1000


class SACLocationData(NamedTuple):
    code: int
    case: str  # Case.name (constants/planets.py) -- single source of truth
    # for this location's planet/operative; regions.py/rules.py both derive
    # those via CASE_NAME_TO_CASE[case] rather than storing them separately.


def all_mission_locations(
    case_name: str, take_id: Callable[[], int],
) -> dict[str, "SACLocationData"]:
    """Missions=all granularity's location set for one case: one location
    per individual CHAPTER_ENTRIES mission belonging to case_name, each
    getting its own id from take_id (a case file's own _take_id()) --
    the finer-grained alternative to that same case file's *_MISSION_
    LOCATIONS single "{case_name} Complete" entry (Missions=
    level_completion). Empty dict if case_name has no CHAPTER_ENTRIES
    (none currently, but tolerated rather than assumed)."""
    return {
        entry.name: SACLocationData(take_id(), case_name)
        for entry in CHAPTER_ENTRIES.get(case_name, ())
    }

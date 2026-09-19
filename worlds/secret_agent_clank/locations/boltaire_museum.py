"""All locations tied to Boltaire Museum, grouped into 4 dicts by which options.py toggle (if any) gates them -- see locations/__init__.py for how these get merged/re-derived for regions.py."""
from ..constants import (
    ALIEN_CODES_BY_CASE,
    CASE_NAME_TO_CASE,
    CLANK_GADGET_BY_CASE_ID,
    CUTSCENE_TO_CASE,
    GADGETBOT_CHALLENGES_BY_CASE,
    GADGETS_BY_CASE,
    KEYCARDS_BY_CASE,
    RATCHET_CHALLENGES_BY_CASE,
    SKILL_POINTS_BY_CASE,
    SPECIAL_CHALLENGES_BY_CASE,
    WEAPONS_BY_CASE,
    SACCases,
)
from ._shared import BASE_ID, CASE_ID_BLOCK_SIZE, SACLocationData, all_mission_locations

_CASE_NAME = SACCases.BOLTAIRE_MUSEUM
_CASE_ID = CASE_NAME_TO_CASE[_CASE_NAME].case_id
_next_id = BASE_ID + (_CASE_ID - 1) * CASE_ID_BLOCK_SIZE


def _take_id() -> int:
    global _next_id
    taken, _next_id = _next_id, _next_id + 1
    return taken


BOLTAIRE_MUSEUM_LOCATIONS: dict[str, SACLocationData] = {}
for _name in WEAPONS_BY_CASE.get(_CASE_NAME, ()):
    BOLTAIRE_MUSEUM_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)
for _name in GADGETS_BY_CASE.get(_CASE_NAME, ()):
    BOLTAIRE_MUSEUM_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)
for _gadget_name in CLANK_GADGET_BY_CASE_ID.get(_CASE_ID, ()):
    BOLTAIRE_MUSEUM_LOCATIONS[f"{_gadget_name} (Pickup)"] = SACLocationData(_take_id(), _CASE_NAME)
for _name in (
    *GADGETBOT_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
    *SPECIAL_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
    *RATCHET_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
):
    BOLTAIRE_MUSEUM_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)

BOLTAIRE_MUSEUM_MISSION_LOCATIONS: dict[str, SACLocationData] = {
    f"Mission: {_CASE_NAME} Complete": SACLocationData(_take_id(), _CASE_NAME),
}

BOLTAIRE_MUSEUM_ALL_MISSIONS_LOCATIONS: dict[str, SACLocationData] = all_mission_locations(_CASE_NAME, _take_id)

BOLTAIRE_MUSEUM_CUTSCENE_LOCATIONS: dict[str, SACLocationData] = {
    _cutscene_name: SACLocationData(_take_id(), _CASE_NAME)
    for _cutscene_name, _case_name in CUTSCENE_TO_CASE.items() if _case_name == _CASE_NAME
}

BOLTAIRE_MUSEUM_OTHER_LOCATIONS: dict[str, SACLocationData] = {}
for _name in (
    *SKILL_POINTS_BY_CASE.get(_CASE_NAME, ()),
    *KEYCARDS_BY_CASE.get(_CASE_NAME, ()),
    *ALIEN_CODES_BY_CASE.get(_CASE_NAME, ()),
):
    BOLTAIRE_MUSEUM_OTHER_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)

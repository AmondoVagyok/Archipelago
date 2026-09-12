"""All locations tied to Rooftop Deathtrap, grouped into 4 dicts by which
options.py toggle (if any) gates them -- see locations/__init__.py for how
these get merged/re-derived for regions.py. Location ids come from this
case's own fixed id block (see locations/_shared.py) so this file is fully
self-contained -- no import-order dependency on sibling case files or on
locations/__init__.py itself.

  - ROOFTOP_DEATHTRAP_LOCATIONS: always created (weapon vendor / gadget pickup /
    gadgetbot / special / ratchet challenge entries for this case).
  - ROOFTOP_DEATHTRAP_MISSION_LOCATIONS: level_completion granularity (default), gated by Missions.
  - ROOFTOP_DEATHTRAP_ALL_MISSIONS_LOCATIONS: all granularity, gated by Missions.
  - ROOFTOP_DEATHTRAP_CUTSCENE_LOCATIONS: gated by AllCutscenes.
  - ROOFTOP_DEATHTRAP_OTHER_LOCATIONS: this case's skill points + keycards + alien
    codes -- each is individually gated by its own option (SkillPoints /
    AllKeycards / AllAlienCodes), so locations/__init__.py re-splits this
    back out by exact display name against constants/*.py rather than
    treating it as one opaque toggle (which option gates a given name
    can't be recovered from this dict alone once merged)."""
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

_CASE_NAME = SACCases.ROOFTOP_DEATHTRAP
_CASE_ID = CASE_NAME_TO_CASE[_CASE_NAME].case_id
_next_id = BASE_ID + (_CASE_ID - 1) * CASE_ID_BLOCK_SIZE


def _take_id() -> int:
    global _next_id
    taken, _next_id = _next_id, _next_id + 1
    return taken


ROOFTOP_DEATHTRAP_LOCATIONS: dict[str, SACLocationData] = {}
for _name in WEAPONS_BY_CASE.get(_CASE_NAME, ()):
    ROOFTOP_DEATHTRAP_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)
for _name in GADGETS_BY_CASE.get(_CASE_NAME, ()):
    ROOFTOP_DEATHTRAP_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)
if _CASE_ID in CLANK_GADGET_BY_CASE_ID:
    _pickup_name = f"{CLANK_GADGET_BY_CASE_ID[_CASE_ID]} (Pickup)"
    ROOFTOP_DEATHTRAP_LOCATIONS[_pickup_name] = SACLocationData(_take_id(), _CASE_NAME)
for _name in (
    *GADGETBOT_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
    *SPECIAL_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
    *RATCHET_CHALLENGES_BY_CASE.get(_CASE_NAME, ()),
):
    ROOFTOP_DEATHTRAP_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)

ROOFTOP_DEATHTRAP_MISSION_LOCATIONS: dict[str, SACLocationData] = {
    f"{_CASE_NAME} Complete": SACLocationData(_take_id(), _CASE_NAME),
}

ROOFTOP_DEATHTRAP_ALL_MISSIONS_LOCATIONS: dict[str, SACLocationData] = all_mission_locations(_CASE_NAME, _take_id)

ROOFTOP_DEATHTRAP_CUTSCENE_LOCATIONS: dict[str, SACLocationData] = {
    _cutscene_name: SACLocationData(_take_id(), _CASE_NAME)
    for _cutscene_name, _case_name in CUTSCENE_TO_CASE.items() if _case_name == _CASE_NAME
}

ROOFTOP_DEATHTRAP_OTHER_LOCATIONS: dict[str, SACLocationData] = {}
for _name in (
    *SKILL_POINTS_BY_CASE.get(_CASE_NAME, ()),
    *KEYCARDS_BY_CASE.get(_CASE_NAME, ()),
    *ALIEN_CODES_BY_CASE.get(_CASE_NAME, ()),
):
    ROOFTOP_DEATHTRAP_OTHER_LOCATIONS[_name] = SACLocationData(_take_id(), _CASE_NAME)

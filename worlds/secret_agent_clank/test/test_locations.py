import unittest

from ..constants import SACCases, SACPickups
from ..constants.cutscenes import CUTSCENE_FLAGS
from ..constants.planets import ALL_CASES, CASE_NAME_TO_PLANET
from ..constants.vendor import VENDOR_WEAPONS, vendor_location_name
from ..constants.weapon_mods import CHALLENGE_MOD_IDS, WEAPON_MODS
from ..locations import (
    ALL_LOCATIONS,
    BASE_ID,
    BASE_VENDOR_LOCATIONS,
    CASE_LOCATIONS,
    CASE_REGIONS,
    LOCATION_NAME_TO_ID,
    LOCATIONS,
    MOD_VENDOR_LOCATIONS,
)


class LocationRecordTests(unittest.TestCase):
    def test_names_and_codes_are_unique(self):
        self.assertEqual(len(ALL_LOCATIONS), len(LOCATIONS))
        self.assertEqual(list(LOCATION_NAME_TO_ID), [location.name for location in LOCATIONS])
        self.assertEqual(sorted(LOCATION_NAME_TO_ID.values()),
                         list(range(BASE_ID, BASE_ID + len(LOCATIONS))))

    def test_every_case_has_exactly_one_region(self):
        self.assertEqual(sorted(CASE_REGIONS), sorted(case.name for case in ALL_CASES))
        for case_name, region in CASE_REGIONS.items():
            self.assertEqual(region.planet, CASE_NAME_TO_PLANET[case_name])
            for location in region.locations:
                self.assertEqual(location.case, case_name)

    def test_vendor_sources_are_not_pickups(self):
        self.assertEqual(set(BASE_VENDOR_LOCATIONS), {vendor_location_name(name) for name in VENDOR_WEAPONS})
        self.assertFalse(set(BASE_VENDOR_LOCATIONS) & {loc.name for loc in CASE_LOCATIONS})
        for mod in WEAPON_MODS:
            self.assertEqual(mod.location in MOD_VENDOR_LOCATIONS, mod.mod_id not in CHALLENGE_MOD_IDS)

    def test_nonexistent_cutscenes_are_removed_from_polling_and_generation(self):
        for name in ALL_LOCATIONS.keys() | CUTSCENE_FLAGS.keys():
            self.assertFalse("Asyanica Rooftops: Enter Cutscene" in name)
            self.assertFalse("Spaceship Graveyard: Enter Cutscene" in name)

    def test_rooftop_pickups_belong_to_clank_case(self):
        for name in (SACPickups.ASYANICA_ROOFTOPS_OMNI_KEY, SACPickups.ASYANICA_ROOFTOPS_CUFFLINK_BOMB,
                     SACPickups.ASYANICA_ROOFTOPS_MINE_LAUNCHER):
            self.assertEqual(ALL_LOCATIONS[name].case, SACCases.ASYANICA_ROOFTOPS)

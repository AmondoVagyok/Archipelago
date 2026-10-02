from ..constants.vendor import vendor_location_name
import unittest

from ..constants.planets import CASE_NAME_TO_PLANET
from ..locations import ALL_LOCATIONS, CASE_LOCATIONS, LOCATIONS


class LocationRecordTests(unittest.TestCase):
    def test_names_and_codes_are_unique(self):
        self.assertEqual(len(ALL_LOCATIONS), len(LOCATIONS))
        self.assertEqual(len({location.code for location in LOCATIONS}), len(LOCATIONS))

    def test_case_locations_link_their_case_and_planet(self):
        for location in CASE_LOCATIONS:
            with self.subTest(location.name):
                self.assertEqual(CASE_NAME_TO_PLANET[location.case], location.planet)

    def test_vendor_sources_are_not_pickups(self):
        from ..constants.vendor import VENDOR_WEAPONS
        from ..constants.weapon_mods import CHALLENGE_MOD_IDS, WEAPON_MODS
        from ..locations import BASE_VENDOR_LOCATIONS, MOD_VENDOR_LOCATIONS
        self.assertEqual(set(BASE_VENDOR_LOCATIONS), {vendor_location_name(name) for name in VENDOR_WEAPONS})
        self.assertFalse(set(BASE_VENDOR_LOCATIONS) & {loc.name for loc in CASE_LOCATIONS})
        for mod in WEAPON_MODS:
            self.assertEqual(mod.location in MOD_VENDOR_LOCATIONS, mod.mod_id not in CHALLENGE_MOD_IDS)

    def test_nonexistent_cutscenes_are_removed_from_polling_and_generation(self):
        from ..constants.cutscenes import CUTSCENES
        for name in ALL_LOCATIONS.keys() | {str(cutscene) for cutscene in CUTSCENES}:
            self.assertFalse("Asyanica Rooftops: Enter Cutscene" in name)
            self.assertFalse("Spaceship Graveyard: Enter Cutscene" in name)

    def test_rooftop_pickups_belong_to_clank_case(self):
        from ..constants import SACCases, SACClankGadgets, SACClankWeapons, SACRatchetWeapons
        for name in (SACClankGadgets.OMNIKEY, SACClankWeapons.CUFFLINK, SACRatchetWeapons.MINELAUNCHER):
            self.assertEqual(ALL_LOCATIONS[name].case, SACCases.ASYANICA_ROOFTOPS)

import unittest
from unittest.mock import patch

from BaseClasses import CollectionState
from rule_builder.rules import False_, Has
from test.general import gen_steps, setup_multiworld
from worlds.AutoWorld import call_all

from ..constants import CASE_NAME_TO_INFOBOT
from ..constants.clank_gadgets import SACClankGadgets, SACClankWeapons
from ..constants.planets import ALL_CASES, SACCases
from ..constants.weapon_progression import TITAN_LOCATIONS
from ..constants.weapons import SACRatchetWeapons
from ..rules import vendor_access
from ..world import SecretAgentClankWorld


def setup_vendor_world(world_type, options=None):
    # Pin Museum for these vendor-route tests; production starts are random.
    m = setup_multiworld(world_type, steps=("generate_early", "create_regions"), options={
        "starting_weapons": 0, "starting_gadgets": 0, **(options or {})})
    museum = next(case for case in ALL_CASES if case.name == SACCases.BOLTAIRE_MUSEUM)
    with patch.object(m.worlds[1].random, "choice", return_value=museum):
        for step in gen_steps[2:]:
            call_all(m, step)
    return m


class VendorAccessTests(unittest.TestCase):
    def test_seed_options_filter_shared_catalog(self):
        from ..constants.vendor import NG_PLUS_VENDOR_ITEMS
        from ..constants.weapon_mods import VENDOR_MODS
        for ng_plus in (0, 1, 2):
            for operatives in ({"Clank": 1}, {"Clank": 1, "Ratchet": 1}):
                with self.subTest(ng_plus=ng_plus, operatives=operatives):
                    m = setup_vendor_world(SecretAgentClankWorld, options={
                        "ng_plus": ng_plus, "operatives": operatives})
                    names = {loc.name for loc in m.get_region("Vendor", 1).locations}
                    for name in NG_PLUS_VENDOR_ITEMS:
                        enabled = bool(ng_plus) and (name.endswith("(Clank)") or "Ratchet" in operatives)
                        self.assertEqual(name in names, enabled, name)
                    if "Ratchet" not in operatives:
                        self.assertFalse(any("(Ratchet)" in name for name in names))
                    for mod in VENDOR_MODS:
                        enabled = bool(ng_plus) if mod.ng_plus else "Ratchet" in operatives
                        self.assertEqual(mod.location in names, enabled, mod.location)
                    self.assertEqual(len(m.itempool), len(m.get_unfilled_locations(1)))

    def test_titan_only_requires_a_reachable_vendor(self):
        requirements = {name: False_() for name in vendor_access.VENDOR_REQUIREMENTS}
        requirements[SACCases.ASYANICA_ROOFTOPS] = Has(SACClankGadgets.JETBOOTS)
        with patch.dict(vendor_access.VENDOR_REQUIREMENTS, requirements, clear=True):
            m = setup_vendor_world(SecretAgentClankWorld, options={"ng_plus": 1})
        world = m.worlds[1]
        state = CollectionState(m)
        titan = m.get_location(TITAN_LOCATIONS["blaster"], 1)
        self.assertFalse(titan.can_reach(state))
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.ASYANICA_ROOFTOPS]))
        state.collect(world.create_item(SACClankGadgets.JETBOOTS))
        self.assertTrue(titan.can_reach(state))
        self.assertFalse(m.get_location(SACRatchetWeapons.BLASTER, 1).can_reach(state))
        self.assertFalse(state.has(SACRatchetWeapons.BLASTER, 1))

    def test_normal_vendor_check_inherits_shared_item_gate(self):
        requirements = {name: False_() for name in vendor_access.VENDOR_REQUIREMENTS}
        requirements[SACCases.BOLTAIRE_MUSEUM] = Has(SACClankGadgets.JETBOOTS)
        with patch.dict(vendor_access.VENDOR_REQUIREMENTS, requirements, clear=True):
            m = setup_vendor_world(SecretAgentClankWorld)
        state = CollectionState(m)
        location = m.get_location(SACClankWeapons.HOLOKNUCKLES, 1)
        self.assertFalse(location.can_reach(state))
        state.collect(m.worlds[1].create_item(SACClankGadgets.JETBOOTS))
        self.assertTrue(location.can_reach(state))

    def test_all_purchase_types_share_one_vendor_without_case_gates(self):
        from ..constants.weapon_mods import VENDOR_MODS
        requirements = {name: False_() for name in vendor_access.VENDOR_REQUIREMENTS}
        requirements[SACCases.ASYANICA_ROOFTOPS] = Has(SACClankGadgets.JETBOOTS)
        with patch.dict(vendor_access.VENDOR_REQUIREMENTS, requirements, clear=True):
            m = setup_vendor_world(SecretAgentClankWorld, options={"ng_plus": 1})
        world = m.worlds[1]
        state = CollectionState(m)
        names = (SACRatchetWeapons.SHOCKROCKET, SACClankGadgets.BOLTGRABBER,
                 SACClankGadgets.CLANKPDA, TITAN_LOCATIONS["shockrocket"], VENDOR_MODS[0].location)
        for name in names:
            self.assertEqual(m.get_location(name, 1).parent_region.name, "Vendor")
            self.assertFalse(m.get_location(name, 1).can_reach(state))
        state.collect(world.create_item(CASE_NAME_TO_INFOBOT[SACCases.ASYANICA_ROOFTOPS]))
        state.collect(world.create_item(SACClankGadgets.JETBOOTS))
        for name in names:
            self.assertTrue(m.get_location(name, 1).can_reach(state), name)
        self.assertFalse(state.has(SACRatchetWeapons.SHOCKROCKET, 1))
        self.assertFalse(state.has(CASE_NAME_TO_INFOBOT[SACCases.INSIDE_THE_A_EYE], 1))

    def test_reported_four_checks_reachable_with_all_items(self):
        m = setup_vendor_world(SecretAgentClankWorld, options={"ng_plus": 1})
        state = m.get_all_state(False)
        for name in (SACClankGadgets.CLANKPDA, SACRatchetWeapons.SHOCKROCKET,
                     SACClankGadgets.BOLTGRABBER, TITAN_LOCATIONS["shockrocket"]):
            self.assertTrue(m.get_location(name, 1).can_reach(state), name)
        self.assertEqual(len(m.itempool), len(m.get_unfilled_locations(1)))

import unittest

from test.general import setup_multiworld

from ..constants.operatives import ALL_OPERATIVES, SACOperatives
from ..constants.planets import SACCases
from ..constants.skillpoints import SKILL_POINTS, SACSkillPointLocations as Locations
from ..constants.skill_point_requirements import (
    EASY_SKILL_POINTS, HARD_SKILL_POINTS, SKILL_POINT_REQUIREMENTS,
)
from ..locations import SKILL_POINT_LOCATIONS
from ..options import SkillPoints
from ..universal_tracker import setup_options_from_slot_data
from ..world import SecretAgentClankWorld


class SkillPointTests(unittest.TestCase):
    def test_every_point_has_one_tier_and_matching_gameplay_case(self):
        self.assertFalse(EASY_SKILL_POINTS & HARD_SKILL_POINTS)
        self.assertEqual(EASY_SKILL_POINTS | HARD_SKILL_POINTS,
                         {point.event_name for point in SKILL_POINTS})
        self.assertEqual(len(SKILL_POINT_REQUIREMENTS), 65)
        self.assertEqual(SKILL_POINT_REQUIREMENTS.keys(), SKILL_POINT_LOCATIONS.keys())
        for name, requirement in SKILL_POINT_REQUIREMENTS.items():
            self.assertEqual(requirement.case, SKILL_POINT_LOCATIONS[name].case)

    def test_option_legacy_booleans_and_new_values(self):
        for value, expected in ((True, 2), (False, 0), ("true", 2), ("false", 0),
                                ("off", 0), ("easy", 1), ("hard", 2), (1, 1), (2, 2)):
            with self.subTest(value=value):
                self.assertEqual(SkillPoints.from_any(value).value, expected)

    def test_generation_tiers_and_each_disabled_operative(self):
        for tier in ("off", "easy", "hard"):
            for disabled in (None, *ALL_OPERATIVES):
                # Exercise both omitted keys and explicit YAML zeroes.
                for explicit_zero in (False, True):
                    enabled = {op: int(op != disabled) for op in ALL_OPERATIVES
                               if op != disabled or explicit_zero}
                    with self.subTest(tier=tier, disabled=disabled, zero=explicit_zero):
                        mw = setup_multiworld(SecretAgentClankWorld, options={
                            "skill_points": tier, "operatives": enabled, "goal": "any",
                        })
                        actual = {loc.name for loc in mw.get_locations(1)} & SKILL_POINT_LOCATIONS.keys()
                        expected = {name for name, req in SKILL_POINT_REQUIREMENTS.items()
                                    if req.difficulty <= SkillPoints.from_any(tier).value
                                    and disabled not in req.operatives}
                        self.assertEqual(actual, expected)

    def test_mixed_mission_and_vault_ownership(self):
        vault = SKILL_POINT_REQUIREMENTS[Locations.GALACTIC_BOLT_RESERVE_VAULT_VAULT]
        self.assertEqual(vault.case, SACCases.INSIDE_THE_A_EYE)
        self.assertEqual(vault.operatives, {SACOperatives.GADGETBOTS})
        casino = SKILL_POINT_REQUIREMENTS[Locations.HIGH_STAKES_ROOM_GADGEBOT_STANDS_ALONE]
        self.assertEqual(casino.operatives, {SACOperatives.SPECIAL_MISSIONS, SACOperatives.GADGETBOTS})
        mw = setup_multiworld(SecretAgentClankWorld, options={"skill_points": "hard"})
        location = mw.get_location(Locations.GALACTIC_BOLT_RESERVE_VAULT_VAULT, 1)
        self.assertEqual(location.parent_region.name, SACCases.INSIDE_THE_A_EYE)
        self.assertEqual(location.address, 77_818_007)

    def test_slot_data_preserves_tier_and_tracker_reads_legacy_booleans(self):
        for value, expected in (("off", 0), ("easy", 1), ("hard", 2), (True, 2), (False, 0)):
            with self.subTest(value=value):
                mw = setup_multiworld(SecretAgentClankWorld, options={"skill_points": value})
                world = mw.worlds[1]
                slot = world.fill_slot_data()
                self.assertIs(type(slot["skill_points"]), int)
                self.assertEqual(slot["skill_points"], expected)
                if isinstance(value, bool):
                    slot["skill_points"] = value
                mw.re_gen_passthrough = {world.game: slot}
                world.options.skill_points.value = -1
                setup_options_from_slot_data(world)
                self.assertEqual(world.options.skill_points.value, expected)

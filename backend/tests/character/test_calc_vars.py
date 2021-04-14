""" Testing for the influence of individual stats and modifies on damage calc """

import unittest

from xivdpscalc.character import Character, CharacterStatSpread
from xivdpscalc.character.jobs import Comp, Jobs

class TestCalcVars(unittest.TestCase): #pylint: disable=missing-class-docstring
    def test_baseline(self):
        """ Baseline test: 5 roles, no raid buffs """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        the_shitters_i_raid_with = Comp(
            {Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.WHM, Jobs.SAM, Jobs.SAM, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(20381.368540000003, test_char.calc_damage(200, the_shitters_i_raid_with))

    def test_applies_comp_penalty(self):
        """ 3 roles, no raid buffs, should be lower than the number in test_baseline """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        # 3 roles, who even needs raid buffs
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WHM, Jobs.SAM})
        # have to manually provide pps for testing for now
        self.assertEqual(19855.659200000002, test_char.calc_damage(200, the_shitters_i_raid_with))

    def test_applies_crit_dh_raid_bonuses(self):
        """ 5 roles, sch and brd for raid buffs, should be higher than test_baseline """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        # DNC not included to isolate confounding variable (tech step)
        the_shitters_i_raid_with = Comp(
            {Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.SAM, Jobs.BRD, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(20685.98776726701, test_char.calc_damage(200, the_shitters_i_raid_with))

    def test_gcd(self):
        """ Test gcd is applying speed correctly """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        self.assertEqual(2.32, test_char.get_gcd())

    def test_base_piety(self):
        """ Test applying piety correctly """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        self.assertEqual(200, test_char.calc_piety())

    def test_dot_scalar(self):
        """ Test speed is applying dot bonus correctly """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        self.assertEqual(1.069, test_char.get_dot_scalar())

    def test_single_raidbuff(self):
        """ Test raid buff is applying damage correctly """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        the_shitters_i_raid_with = Comp(
            {Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.AST, Jobs.SAM, Jobs.SAM, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(20534.228804050006, test_char.calc_damage(200, the_shitters_i_raid_with))

    def test_multiple_raidbuff(self):
        """ Test multiple raid buffs are applying damage correctly """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        the_shitters_i_raid_with = Comp(
            {Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.AST, Jobs.NIN, Jobs.SAM, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(20790.90666410063, test_char.calc_damage(200, the_shitters_i_raid_with))

    def test_embolden_has_no_effect(self):
        """ Test embolden isn't mistakenly applying damage """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        the_shitters_i_raid_with = Comp(
            {Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.WHM, Jobs.SAM, Jobs.SAM, Jobs.MCH, Jobs.RDM})
        # have to manually provide pps for testing for now
        self.assertEqual(20381.368540000003, test_char.calc_damage(200, the_shitters_i_raid_with))

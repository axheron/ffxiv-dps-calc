""" Tests for the scholar pps and mp generation calculators """

import unittest

from xivdpscalc.pps.sch import SchPps, SchAction
from xivdpscalc.pps.sample_sch_rotation import FixedSchRotation, SampleSchRotation
from xivdpscalc.character.jobs import Jobs
from xivdpscalc.character import Character, CharacterStatSpread
from xivdpscalc.pps.sch_action import SchSimNotice

class TestSchCalc(unittest.TestCase):  #pylint: disable=missing-class-docstring
    def test_total_potency(self):
        """ Test the spreadsheet port for total potency """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertAlmostEqual(24326.1264, mypps.total_potency_spreadsheet_port(test_char, 0.12, 4, 0), places=3)

    def test_cycle(self):
        """ Test the spreadsheet port for cycle length """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertAlmostEqual(174.12, mypps.get_cycle(test_char, 0.12), places=2)

    def test_mp(self):
        """ Test the spreadsheet port for mp generation """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertAlmostEqual(508.0952,
                         mypps.get_mp_per_min(test_char, caster_tax=0.1, succ=0, adlo=0, energy_drain=4, rez=0), places=3)
        
    def test_variable_time_sim_allows_weaves(self):
        """ Ensure the time variable sim allows weaving after instant casts """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        # If the sim properly supports weaving, this should be 4 full gcds
        fixed_rotation = [SchAction.BIOLYSIS, SchAction.AETHERFLOW, SchAction.ENERGYDRAIN, SchAction.BROIL3, 
                          SchAction.RUIN2, SchAction.ENERGYDRAIN, SchAction.SWIFTCAST, SchAction.BROIL3, SchAction.ENERGYDRAIN]
        sim_result = mypps.get_total_potency_variable_time(
            test_char.get_gcd() * 4, test_char, FixedSchRotation(fixed_rotation, SchAction.BROIL3), 0.1)
        # 3 ED, 2 B3, 1 R2
        self.assertEqual(1080, sim_result.get_non_dot_potency())
        
    def test_variable_time_sim_notes_af_overspending(self):
        """ Ensure the time variable sim allows weaving after instant casts """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        # Burn an aetherflow we don't have
        fixed_rotation = [SchAction.ENERGYDRAIN]
        sim_result = mypps.get_total_potency_variable_time(
            1, test_char, FixedSchRotation(fixed_rotation, SchAction.BROIL3), 0.1)
        # 3 ED, 2 B3, 1 R2
        self.assertIn(SchSimNotice.SCH_SIM_AETHERFLOW_OVERSPENDING, sim_result.notices)
        
    def test_sample_sch_rotation_correct_casts(self):
        """ Ensure the time variable sim allows weaving after instant casts """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        # in 2 minutes on a 4th gcd chain opener, youd have: 2 AF, 9 ED, 1 CS, 1 SC, 1 Diss, 4 bio, 3 R2, 42 B3
        sim_result = mypps.get_total_potency_variable_time(120, test_char, SampleSchRotation(), 0.1)
        self.assertEqual(len(sim_result.timeline[SchAction.AETHERFLOW]), 2)
        self.assertEqual(len(sim_result.timeline[SchAction.ENERGYDRAIN]), 9)
        self.assertEqual(len(sim_result.timeline[SchAction.CHAINSTRATAGEM]), 1)
        self.assertEqual(len(sim_result.timeline[SchAction.SWIFTCAST]), 2)
        self.assertEqual(len(sim_result.timeline[SchAction.DISSIPATION]), 1)
        self.assertEqual(len(sim_result.timeline[SchAction.BIOLYSIS]), 4)
        self.assertEqual(len(sim_result.timeline[SchAction.RUIN2]), 3)
        self.assertEqual(len(sim_result.timeline[SchAction.BROIL3]), 42)

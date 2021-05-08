""" Tests for the scholar pps and mp generation calculators """

import unittest

from xivdpscalc.pps.sch import SchPps
from xivdpscalc.pps.sample_sch_rotation import FixedSchRotation
from xivdpscalc.character import Character, CharacterStatSpread, Jobs
from xivdpscalc.pps.sch_action import SchAction

class TestSchRotation(unittest.TestCase):  #pylint: disable=missing-class-docstring
    def test_sim_allows_weaves(self):
        """ Ensure the time variable sim allows weaving after instant casts """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        # If the sim properly supports weaving, this should be 4 full gcds
        fixed_rotation = [SchAction.BIOLYSIS, SchAction.AETHERFLOW, SchAction.ENERGYDRAIN, SchAction.BROIL3, 
                          SchAction.RUIN2, SchAction.ENERGYDRAIN, SchAction.SWIFTCAST, SchAction.BROIL3, SchAction.ENERGYDRAIN]
        # 3 ED, 2 B3, 1 R2
        self.assertEqual(1080, mypps.get_total_potency_variable_time(
            test_char.get_gcd() * 4, test_char, FixedSchRotation(fixed_rotation, SchAction.BROIL3), 0.1))

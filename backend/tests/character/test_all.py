""" End to end damage calc testing """

import unittest

from xivdpscalc.character import Character, CharacterStatSpread
from xivdpscalc.character.jobs import Comp, Jobs


class TestEndToEnd(unittest.TestCase):  #pylint: disable=missing-class-docstring
    def test_scholar(self):
        """ E2E scholar damage calc test """
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        my_character = Character(Jobs.SCH, my_stat_spread)
        test_comp = \
            Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.WHM, Jobs.SAM, Jobs.SAM, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertAlmostEqual(14238.0411, my_character.calc_damage(139.71, test_comp), places=3)

import unittest

from calc import CharacterStats, Comp, Jobs


class TestEndToEnd(unittest.TestCase):

    def test_scholar(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.WHM, Jobs.SAM, Jobs.SAM, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(me.calc_damage(139.71, the_shitters_i_raid_with), 14238.04118)

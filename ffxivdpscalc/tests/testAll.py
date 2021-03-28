import unittest

from ffxivdpscalc.calc import CharacterStats, Comp, Jobs


class TestEndToEnd(unittest.TestCase):

    def test_scholar(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.AST, Jobs.SAM, Jobs.NIN, Jobs.MCH, Jobs.SMN})
        # have to manually provide py for testing for now
        self.assertEqual(me.calc_damage(139.71, the_shitters_i_raid_with), 14238.04118)

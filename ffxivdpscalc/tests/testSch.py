import unittest, math

from ffxivdpscalc.classimpl.sch import SchCharacterStats
from ffxivdpscalc.calc import Jobs


class TestSchCalc(unittest.TestCase):

    def test_total_potency(self):
        me = SchCharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        self.assertEqual(me.pps_spreadsheet_port(0.12, 4), 24326.1264)
    
    def test_cycle(self):
        me = SchCharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        self.assertEqual(me.get_cycle(0.12), 174.12)
import unittest, math

from ffxivdpscalc.pps.sch import SchPps
from ffxivdpscalc.calc import Jobs, CharacterStats


class TestSchCalc(unittest.TestCase):

    def test_total_potency(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.total_potency_spreadsheet_port(me, 0.12), 24326.1264)
    
    def test_cycle(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.get_cycle(me, 0.12), 174.12)

import unittest, math

from backend.pps.sch import SchPps
from backend.calc import Jobs, CharacterStats


class TestSchCalc(unittest.TestCase):

    def test_total_potency(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.total_potency_spreadsheet_port(me, 0.12, 4, 0), 24326.1264)
    
    def test_cycle(self):
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.get_cycle(me, 0.12), 174.12)

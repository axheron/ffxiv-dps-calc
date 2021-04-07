import unittest, math

from backend.pps.sch import SchPps
from backend.character.jobs import Jobs
from backend.character.character import Character


class TestSchCalc(unittest.TestCase):

    def test_total_potency(self):
        me = Character(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.total_potency_spreadsheet_port(me, 0.12, 4, 0), 24326.1264)
    
    def test_cycle(self):
        me = Character(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.get_cycle(me, 0.12), 174.12)

    def test_mp(self):
        me = Character(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        mypps = SchPps()
        self.assertEqual(mypps.get_mp_per_min(me, caster_tax=0.1, succ=0, adlo=0, ed=4, rez=0), 508.0952931652587)
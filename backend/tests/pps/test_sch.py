import unittest, math

from backend.pps.sch import SchPps
from backend.character.jobs import Jobs
from backend.character.character import Character, CharacterStatSpread


class TestSchCalc(unittest.TestCase):

    def test_total_potency(self):
        ''' Test the spreadsheet port for total potency '''
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertEqual(mypps.total_potency_spreadsheet_port(test_char, 0.12, 4, 0), 24326.1264)

    def test_cycle(self):
        ''' Test the spreadsheet port for cycle length '''
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertEqual(mypps.get_cycle(test_char, 0.12), 174.12)

    def test_mp(self):
        ''' Test the spreadsheet port for mp generation '''
        my_stat_spread = CharacterStatSpread(
            wd=180, mainstat=5577, det=2272, crit=3802, dh=1100, speed=2139, ten=380, pie=340)
        test_char = Character(Jobs.SCH, my_stat_spread)
        mypps = SchPps()
        self.assertEqual(mypps.get_mp_per_min(
            test_char, caster_tax=0.1, succ=0, adlo=0, ed=4, rez=0), 508.0952931652587)

import unittest

from ffxivdpscalc.calc import CharacterStats, Comp, Jobs


class TestCalcVars(unittest.TestCase):
    
    def test_baseline(self):
        # Baseline test: 5 roles, no raid buffs
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.AST, Jobs.SAM, Jobs.NIN, Jobs.MCH, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(me.calc_damage(200, the_shitters_i_raid_with), 20381.368540000003)
    
    def test_applies_comp_penalty(self):
        # 3 roles, no raid buffs, should be lower than the number in test_baseline
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        # 3 roles, who even needs raid buffs
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WHM, Jobs.SAM})
        # have to manually provide pps for testing for now
        self.assertEqual(me.calc_damage(200, the_shitters_i_raid_with), 19855.659200000002)

    def test_applies_crit_dh_raid_bonuses(self):
        # 5 roles, sch and brd for raid buffs, should be higher than test_baseline
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        # DNC not included to isolate confounding variable (tech step)
        the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.SAM, Jobs.BRD, Jobs.BLM})
        # have to manually provide pps for testing for now
        self.assertEqual(me.calc_damage(200, the_shitters_i_raid_with), 20608.705123055555)
        
    def test_gcd(self):
        # 5 roles, sch and brd for raid buffs, should be higher than test_baseline
        me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
        self.assertEqual(me.get_gcd(), 2.32)
        
        #todo: Add testing for raid dmg buffs (tech, div, etc) once implemented
        
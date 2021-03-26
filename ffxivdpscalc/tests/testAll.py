from ffxivdpscalc.main import CharacterStats, Comp, Jobs


def run_test():
    me = CharacterStats(Jobs.SCH, 180, 5577, 2272, 3802, 1100, 2139, 380, 340)
    the_shitters_i_raid_with = Comp({Jobs.PLD, Jobs.WAR, Jobs.SCH, Jobs.AST, Jobs.SAM, Jobs.NIN, Jobs.MCH, Jobs.SMN})
    # have to manually provide pps for testing for now
    print(me.calc_damage(139.71, the_shitters_i_raid_with))

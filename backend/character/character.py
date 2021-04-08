""" Representation of a single character and its stat spread """

import math
from dataclasses import dataclass
from character.stat import Stat, Stats, ProbabalisticStat
from character.jobs import Roles, Buffs

@dataclass
class CharacterStatSpread: #pylint: disable=too-many-instance-attributes
    """
    Value class representation of a stat spread
    """
    wd: float #pylint: disable=invalid-name
    mainstat: int
    det: int
    crit: int
    dh: int #pylint: disable=invalid-name
    speed: int
    ten: int
    pie: int

class Character:
    """
    The main class where damage is calculated. Initialized by providing a CharacterStatSpread.
    """
    def __init__(self, job, stat_spread):
        self.job = job
        self.wd = stat_spread.wd  #pylint: disable=invalid-name
        self.stats = {}
        self.stats[Stats.MAINSTAT] = Stat(Stats.MAINSTAT, stat_spread.mainstat)
        self.stats[Stats.DET] = Stat(Stats.DET, stat_spread.det)
        self.stats[Stats.CRIT] = ProbabalisticStat(Stats.CRIT, stat_spread.crit)
        self.stats[Stats.DH] =  ProbabalisticStat(Stats.DH, stat_spread.dh)
        self.stats[Stats.SPEED] = Stat(Stats.SPEED, stat_spread.speed)
        self.stats[Stats.TEN] = Stat(Stats.TEN, stat_spread.ten)
        self.stats[Stats.PIE] = Stat(Stats.PIE, stat_spread.pie)

    def get_gcd(self):
        """
        Returns the character's gcd given its skill or spell speed
        :return: the gcd in seconds
        """
        return math.floor(0.25 * (1000 - self.stats[Stats.SPEED].get_multiplier())) / 100

    def get_dot_scalar(self):
        """
        Returns the character's dot damage bonus, given its skill or spell speed
        :return: the modified dot multiplier
        """
        return  1 + (self.stats[Stats.SPEED].get_multiplier() / 1000)

    def calc_piety(self):
        """
        Returns the character's mp regen resulting from the piety stat
        :return: ??? (Is this mp per 3 seconds?  I'm not sure)
        """
        return 200 + self.stats[Stats.PIE].get_multiplier()

    # comp is a Comp() object
    # todo: break this up neatly
    def calc_damage(self, potency, comp, is_dot=False, crit_rate=None, dh_rate=None):  #pylint: disable=too-many-arguments, too-many-locals
        """
        Calculates the estimated DPS based on the team composition and current character stats
        :param potency: Potency calculated on expected rotation
        :param comp: Team composition.
        :param is_dot: ???
        :param crit_rate: ???
        :param dh_rate: ???
        :return: the DPS number
        """
        # modify mainstat according to number of roles
        modified_mainstat = Stat(Stats.MAINSTAT, math.floor(self.stats[Stats.MAINSTAT].value * (
            1 + 0.01 * comp.n_roles)))

        # damage effect of non-probabalistic stats
        job_mod_scaling = (340 * self.job.job_mod // 1000)
        damage = potency * (
            self.wd + job_mod_scaling) * (100 + modified_mainstat.get_multiplier()) // 100
        damage = self.stats[Stats.DET].apply_stat(damage)
        damage = self.stats[Stats.TEN].apply_stat(damage)
        if is_dot:
            damage = self.stats[Stats.SPEED].apply_stat(damage)

        damage //= 100  # why? i do not know. cargo culted

        # damage effect of job traits / stance
        # todo: pull out traits
        if self.job.role == Roles.HEALER:
            damage = math.floor(damage * 1.3)  # magic and mend

        # damage effect of probabalistic stats
        crit_damage = self.stats[Stats.CRIT].apply_stat(damage)
        dh_damage = damage * self.stats[Stats.DH].stat.m_factor // 1000
        cdh_damage = crit_damage * self.stats[Stats.DH].stat.m_factor // 1000

        # use expected crit rate based on stats if none is supplied
        if not crit_rate:
            crit_rate = self.stats[Stats.CRIT].get_p()
        if not dh_rate:
            dh_rate = self.stats[Stats.DH].get_p()

        # apply party crit/dh buffs
        for buff in comp.raidbuffs:
            if buff in Buffs.crit_buffs():
                crit_rate += buff.avg_buff_effect(self.job)
            elif buff in Buffs.dh_buffs():
                dh_rate += buff.avg_buff_effect(self.job)

        cdh_rate = crit_rate * dh_rate
        normal_rate = 1 - crit_rate - dh_rate + cdh_rate
        expected_damage = damage * normal_rate + (
            crit_damage * (crit_rate - cdh_rate)) + (
            dh_damage * (dh_rate - cdh_rate)) + (
            cdh_damage * cdh_rate)

        for buff in comp.raidbuffs:
            if buff in Buffs.raid_buffs():
                expected_damage *= (1 + buff.avg_buff_effect(self.job))

        return expected_damage

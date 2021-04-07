''' Representation of a single character and its stat spread '''

import math
from backend.character.stat import Stat, Stats, ProbabalisticStat
from backend.character.jobs import Roles, Buffs, Jobs
from dataclasses import dataclass

@dataclass
class CharacterStatSpread:
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
    def __init__(self, job, stat_spred):
        self.job = job
        self.wd = stat_spred.wd  #pylint: disable=invalid-name
        self.mainstat = Stat(Stats.MAINSTAT, stat_spred.mainstat)
        self.det = Stat(Stats.DET, stat_spred.det)
        self.crit = ProbabalisticStat(Stats.CRIT, stat_spred.crit)
        self.dh = ProbabalisticStat(Stats.DH, stat_spred.dh)  #pylint: disable=invalid-name
        self.speed = Stat(Stats.SPEED, stat_spred.speed)
        self.ten = Stat(Stats.TEN, stat_spred.ten)
        self.pie = Stat(Stats.PIE, stat_spred.pie)

    def get_gcd(self):
        '''
        Returns the character's gcd given its skill or spell speed
        :return: the gcd in seconds
        '''
        return math.floor(0.25 * (1000 - self.speed.get_multiplier())) / 100

    def get_dot_scalar(self):
        '''
        Returns the character's dot damage bonus, given its skill or spell speed
        :return: the modified dot multiplier
        '''
        return  1 + (self.speed.get_multiplier() / 1000)

    def calc_piety(self):
        '''
        Returns the character's mp regen resulting from the piety stat
        :return: ??? (Is this mp per 3 seconds?  I'm not sure)
        '''
        return 200 + self.pie.get_multiplier()

    # comp is a Comp() object
    # todo: break this up in a way that doesn't look like an arbitrarily segmented set of function calls
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
        modified_mainstat = Stat(Stats.MAINSTAT, math.floor(self.mainstat.value * (
            1 + 0.01 * comp.n_roles)))

        # damage effect of non-probabalistic stats
        job_mod_scaling = (340 * self.job.job_mod // 1000)
        damage = potency * (
            self.wd + job_mod_scaling) * (100 + modified_mainstat.get_multiplier()) // 100
        damage = self.det.apply_stat(damage)
        damage = self.ten.apply_stat(damage)
        if is_dot:
            damage = self.speed.apply_stat(damage)

        damage //= 100  # why? i do not know. cargo culted

        # damage effect of job traits / stance
        # todo: pull out traits
        if self.job.role == Roles.HEALER:
            damage = math.floor(damage * 1.3)  # magic and mend

        # damage effect of probabalistic stats
        crit_damage = self.crit.apply_stat(damage)
        dh_damage = damage * self.dh.stat.m_factor // 1000
        cdh_damage = crit_damage * self.dh.stat.m_factor // 1000

        # use expected crit rate based on stats if none is supplied
        if not crit_rate:
            crit_rate = self.crit.get_p()
        if not dh_rate:
            dh_rate = self.dh.get_p()

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

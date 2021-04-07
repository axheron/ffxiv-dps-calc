# Representation of a single character and its stat spread

from enum import Enum, auto
from backend.character.stat import Stat, Stats, ProbabalisticStat
from backend.character.jobs import Roles, Buffs, Jobs, Comp
import itertools
import math

class Character:
    def __init__(self, job, wd, mainstat, det, crit, dh, speed, ten, pie):
        self.job = job
        self.wd = wd
        self.mainstat = Stat(Stats.MAINSTAT, mainstat)
        self.det = Stat(Stats.DET, det)
        self.crit = ProbabalisticStat(Stats.CRIT, crit)
        self.dh = ProbabalisticStat(Stats.DH, dh)
        self.speed = Stat(Stats.SPEED, speed)
        self.ten = Stat(Stats.TEN, ten)
        self.pie = Stat(Stats.PIE, pie)

    @classmethod
    def truncate(cls, val, precision=1000):
        return (precision + val) / precision

    @classmethod
    def multiply_and_truncate(cls, val, factor, precision=1000):
        return math.floor(val * cls.truncate(factor, precision))

    @classmethod
    def apply_stat(cls, damage, stat):
        return cls.multiply_and_truncate(damage, stat.get_multiplier())
    
    def get_gcd(self):
        return math.floor(0.25 * (1000 - self.speed.get_multiplier())) / 100
    
    def get_dot_scalar(self):
        return  1 + (self.speed.get_multiplier() / 1000)

    def calc_piety(self):
        return 200 + self.pie.get_multiplier()

    # comp is a Comp() object
    def calc_damage(self, potency, comp, is_dot=False, crit_rate=None, dh_rate=None):
        # modify mainstat according to number of roles
        modified_mainstat = Stat(Stats.MAINSTAT, math.floor(self.mainstat.value * (1 + 0.01 * comp.n_roles)))

        # damage effect of non-probabalistic stats
        damage = potency * (self.wd + (340 * self.job.job_mod // 1000)) * (
                    100 + modified_mainstat.get_multiplier()) // 100;  # cursed tbh
        damage = self.apply_stat(damage, self.det)
        damage = self.apply_stat(damage, self.ten)
        if is_dot: damage = self.apply_stat(damage, self.speed)

        damage //= 100  # why? i do not know. cargo culted

        # damage effect of job traits / stance
        # todo: pull out traits
        if self.job.role == Roles.HEALER: damage = math.floor(damage * 1.3)  # magic and mend

        # damage effect of probabalistic stats
        crit_damage = self.apply_stat(damage, self.crit)
        dh_damage = damage * self.dh.stat.m_factor // 1000
        cdh_damage = crit_damage * self.dh.stat.m_factor // 1000

        # use expected crit rate based on stats if none is supplied
        if not crit_rate: crit_rate = self.crit.get_p()
        if not dh_rate: dh_rate = self.dh.get_p()

        # apply party crit/dh buffs
        for buff in comp.raidbuffs:
            if buff in Buffs.crit_buffs():
                crit_rate += buff.avg_buff_effect(self.job)
            elif buff in Buffs.dh_buffs():
                dh_rate += buff.avg_buff_effect(self.job)

        cdh_rate = crit_rate * dh_rate
        normal_rate = 1 - crit_rate - dh_rate + cdh_rate
        expected_damage = damage * normal_rate + crit_damage * (crit_rate - cdh_rate) + dh_damage * (
                    dh_rate - cdh_rate) + cdh_damage * cdh_rate

        for buff in comp.raidbuffs:
            if buff in Buffs.raid_buffs():
                expected_damage *= (1 + buff.avg_buff_effect(self.job))

        return expected_damage

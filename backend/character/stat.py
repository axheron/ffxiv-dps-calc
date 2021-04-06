# General representation of stats

from enum import Enum, auto
import itertools
import math


class Stats(Enum):
    MAINSTAT = (340, 165, 0)
    DET = (340, 130, 0)
    CRIT = (380, 200, 400)
    DH = (380, 1250, 0)
    SPEED = (380, 130, 0)
    TEN = (380, 100, 0)
    PIE = (340, 1, 0)
    GCD = (2500, 1, 0)  # in milliseconds
    PRECISION = (1000, 1, 0)  # defaulting to 3 digits of precision

    def __init__(self, base, m_factor, m_scalar):
        self.base = base
        self.m_factor = m_factor
        self.m_scalar = m_scalar


class Stat():
    def __init__(self, stat, value):
        self.stat = stat
        self.value = value

    def get_multiplier(self):
        if self.stat == Stats.DH:
            return 1.25

        magic_num = 3300
        if self.stat == Stats.MAINSTAT:
            magic_num = 340  # don't ask me why dude
        delta = self.value - self.stat.base
        return self.stat.m_factor * delta // magic_num + self.stat.m_scalar
    
class ProbabalisticStat(Stat):
    def __init__(self, stat, value):
        super().__init__(stat, value)
        self.p_factor = 1
        self.p_scalar = 0
        if stat == Stats.CRIT:
            self.p_factor = 200
            self.p_scalar = 50
        elif stat == Stats.DH:
            self.p_factor = 550

    def get_p(self):
        delta = self.value - self.stat.base
        return (self.p_factor * delta // 3300 + self.p_scalar) / Stats.PRECISION.base
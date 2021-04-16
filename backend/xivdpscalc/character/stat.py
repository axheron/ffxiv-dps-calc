""" General representation of stats """

from enum import Enum
from typing import ClassVar
import math


class Stats(Enum):
    """
    Contains math factors for each individual stat.
    """
    MAINSTAT = (340, 165, 0)
    DET = (340, 130, 0)
    CRIT = (380, 200, 400)
    DH = (380, 1250, 0)
    SPEED = (380, 130, 0)
    TEN = (380, 100, 0)
    PIE = (340, 150, 0)
    GCD = (2500, 1, 0)  # in milliseconds

    def __init__(self, base: int, m_factor: int, m_scalar: int):
        """
        :param base: the base value for each stat.
        :param m_factor: magic value for magic math, fits the reverse engineered formula.
        :param m_scalar: magic value for magic math, fits the reverse engineered formula.
        """
        self.base = base
        self.m_factor = m_factor
        self.m_scalar = m_scalar

class Stat():
    """
    For each stat, gives a multiplier. Also holds the value of each stat.
    """
    def __init__(self, stat, value):
        """
        :param stat: from Stats enum.
        :param value: the current value of the stat.
        """
        self.stat = stat
        self.value = value

    @classmethod
    def truncate(cls, val, precision=1000):
        """
        Truncate numbers to the specified number of sigfigs
        :returns: the truncated number
        """
        return (precision + val) / precision

    @classmethod
    def multiply_and_truncate(cls, val, factor, precision=1000):
        """
        Returns the truncated result of val * factor
        :returns: the truncated product
        """
        return math.floor(val * cls.truncate(factor, precision))

    def get_multiplier(self):
        """
        Calculates the multiplier based on the stat.
        :returns: A floating point number representing the multiplier.
        """
        if self.stat == Stats.DH:
            return 1.25

        magic_num = 3300
        if self.stat == Stats.MAINSTAT:
            magic_num = 340  # don't ask me why dude
        delta = self.value - self.stat.base
        return self.stat.m_factor * delta // magic_num + self.stat.m_scalar

    def apply_stat(self, damage):
        """
        Applies the stat's multiplier to a damage value
        :returns: the modified damage number
        """
        return self.multiply_and_truncate(damage, self.get_multiplier())

class ProbabalisticStat(Stat):
    """
    Derived from Stat class, used for stats that increase the chance of something happening
    such as critical hit and direct hit.
    """

    # Class variables to convert stats
    P_factors = tuple[int, int]  # for less ugly

    CRIT_CONVERT: ClassVar[dict[Stats, P_factors]] = {
        Stats.CRIT: (200, 50),
        Stats.DH: (550, 0),
    }
    DEFAULT_PSTATS: ClassVar[P_factors] = (1, 0)

    def __init__(self, stat: Stats, value: int, precision=1000):
        """
        :param stat: from Stats enum.
        :param value: the current value of the stat.
        :param p_factor: magic value for reverse engineered damage formula.
        :param p_scalar: magic value for reverse engineered damage formula.
        """
        super().__init__(stat, value)
        self.p_factor, self.p_scalar = ProbabalisticStat.CRIT_CONVERT.get(stat, ProbabalisticStat.DEFAULT_PSTATS)
        self.precision = precision

    def get_p(self):
        """
        Calculates probablistic factor applied to crit and dh for damage formula
        :returns: returns p_factor
        """
        delta = self.value - self.stat.base
        return (self.p_factor * delta // 3300 + self.p_scalar) / self.precision

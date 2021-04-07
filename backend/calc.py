"""
calc.py
Contains mathematical breakdowns of the stats used to calculate damage, and also contains a function
(CharacterStats: calc_damage) to estimate the DPS of a character given the party composition and gear stats.
"""
from __future__ import annotations  # this is for type hinting Comp. Remove when file is split.
from enum import Enum, auto
from dataclasses import dataclass

import itertools
import math
from typing import ClassVar


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
    PRECISION = (1000, 1, 0)  # defaulting to 3 digits of precision

    def __init__(self, base: int, m_factor: int, m_scalar: int):
        """
        :param base: the base value for each stat.
        :param m_factor: magic value for magic math.
        :param m_scalar: magic value for magic math.
        """
        self.base = base
        self.m_factor = m_factor
        self.m_scalar = m_scalar


@dataclass
class Stat:
    """
    For each stat, gives a multiplier. Also holds the value of each stat.
    """
    stat: Stats
    value: int

    def get_multiplier(self) -> float:
        """
        Calculates the multiplier based on the stat.
        :return: A floating point number representing the multiplier.
        """
        if self.stat == Stats.DH:
            return 1.25

        magic_num = 3300
        if self.stat == Stats.MAINSTAT:
            magic_num = 340  # don't ask me why dude
        delta = self.value - self.stat.base
        return self.stat.m_factor * delta // magic_num + self.stat.m_scalar


class ProbabalisticStat(Stat):
    """
    Derived from Stat class, used for stats that increase the chance of something happening such as critical hit and
    direct hit.
    """

    # Class variable to convert stats
    P_scalars = tuple[int, int]  # for less ugly

    CRIT_CONVERT: ClassVar[dict[Stats, P_scalars]] = {
        Stats.CRIT: (200, 50),
        Stats.DH: (550, 0),
    }
    DEFAULT_PSTATS: ClassVar[tuple[int, int]] = (1, 0)

    def __init__(self, stat: Stats, value: int):
        """
        :param stat: from Stats enum.
        :param value: the current value of the stat.
        :param p_factor: magic value for magic math.
        :param p_scalar: magic value for magic math.
        """
        super().__init__(stat, value)
        self.p_factor, self.p_scalar = ProbabalisticStat.CRIT_CONVERT.get(stat, ProbabalisticStat.DEFAULT_PSTATS)

    def get_p(self) -> float:
        """
        :return: returns probablistic value.
        """
        delta = self.value - self.stat.base
        return (self.p_factor * delta // 3300 + self.p_scalar) / Stats.PRECISION.base  # pylint: disable=no-member


class CharacterStats:
    """
    The main class where damage is calculated. Initialized by providing the character's stats.
    """

    # TODO: Consider breaking out a lot of these parameters into a dict since that's a lot of params
    def __init__(self, job: Jobs, wd: int, mainstat: int, det: int, crit: int, dh: int, speed: int, ten: int, pie: int):
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
    def truncate(cls, val: float, precision=1000) -> float:
        """Truncates a value."""
        return (precision + val) / precision

    @classmethod
    def multiply_and_truncate(cls, val: float, factor: float, precision=1000):
        """Multiplies and truncates a value."""
        return math.floor(val * cls.truncate(factor, precision))

    @classmethod
    def apply_stat(cls, damage: float, stat: Stat):
        """Applies stat by multiplying and truncating the value."""
        return cls.multiply_and_truncate(damage, stat.get_multiplier())

    def get_gcd(self):
        """Returns GCD"""
        return math.floor(0.25 * (1000 - self.speed.get_multiplier())) / 100

    def get_dot_scalar(self):
        """Returns dot scalar"""
        return 1 + (self.speed.get_multiplier() / 1000)

    def calc_piety(self):
        """Calculates piety"""
        return 200 + self.pie.get_multiplier()

    def calc_damage(self, potency_per_sec: float, comp: Comp, is_dot=False, crit_rate=None, dh_rate=None) -> float:
        """
        Calculates the estimated DPS based on the team composition and current character stats
        :param potency_per_sec: Potency calculated on expected rotation
        :param comp: Team composition.
        :param is_dot: Whether damage is dot damage.
        :param crit_rate: manual setting for crit rate for calculating a specific proc rate.
        :param dh_rate: manual setting for DH rate for calculating a specific proc rate.
        :return: the DPS number
        """
        # modify mainstat according to number of roles
        modified_mainstat = Stat(Stats.MAINSTAT, math.floor(self.mainstat.value * (1 + 0.01 * comp.n_roles)))

        # damage effect of non-probabalistic stats
        damage = potency_per_sec * (self.wd + (340 * self.job.job_mod // 1000)) * (
                    100 + modified_mainstat.get_multiplier()) // 100  # cursed tbh
        damage = self.apply_stat(damage, self.det)
        damage = self.apply_stat(damage, self.ten)
        if is_dot:
            damage = self.apply_stat(damage, self.speed)

        damage //= 100  # why? i do not know. cargo culted

        # damage effect of job traits / stance
        # todo: pull out traits
        if self.job.role == Roles.HEALER:
            damage = math.floor(damage * 1.3)  # magic and mend

        # damage effect of probabalistic stats
        crit_damage = self.apply_stat(damage, self.crit)
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
        expected_damage = damage * normal_rate + crit_damage * (crit_rate - cdh_rate) + dh_damage * (
                    dh_rate - cdh_rate) + cdh_damage * cdh_rate

        for buff in comp.raidbuffs:
            if buff in Buffs.raid_buffs():
                expected_damage *= (1 + buff.avg_buff_effect(self.job))

        return expected_damage


class Roles(Enum):
    """
    An enum used to calculate the stat bonuses for having one of each role.
    """
    TANK = auto()
    HEALER = auto()
    MELEE = auto()
    RANGED = auto()
    CASTER = auto()


class Buffs(Enum):
    """
    List of all buffs in the game. Each buff has three parameters:

    """
    # aoe
    CHAIN = (0.1, 15, 120)
    DIV = (0.06, 15, 120)  # 3 seal div
    TRICK = (0.05, 15, 60)
    LITANY = (0.1, 20, 180)
    BROTHERHOOD = (0.05, 15, 90)
    BV = (0.2, 20, 180)
    BARD_CRIT = (0.02, 30, 80)
    BARD_DH = (0.03, 20, 80)
    TECH = (0.05, 20, 120)
    DEVOTION = (0.05, 15, 180)
    EMBOLDEN = (0.1, 20, 120)  # need to handle buff decay
    # single target
    CARD = (0.06, 15, 30)
    LORD_LADY = (0.08, 15, 30)
    DSIGHT_SELF = (0.1, 20, 120)
    DSIGHT_OTHER = (0.05, 20, 120)
    DEVILMENT = (0.2, 20, 120)

    # todo: should probably add standard, personal tank buffs

    def __init__(self, multiplier: float, duration_sec: int, cooldown_sec: int):
        """
        :param multiplier: The amount that the damage of the ability is increased.
        :param duration_sec: How long the buff lasts, in seconds.
        :param cooldown_sec: How long until the buff may be used again, in seconds.
        """
        self.multiplier = multiplier
        self.duration_sec = duration_sec
        self.cooldown_sec = cooldown_sec

    @classmethod
    def crit_buffs(cls):
        """returns all critbuffs"""
        return {cls.CHAIN, cls.LITANY, cls.DEVILMENT, cls.BARD_CRIT}

    @classmethod
    def dh_buffs(cls):
        """returns all dhbuffs"""
        return {cls.BV, cls.BARD_DH, cls.DEVILMENT}

    @classmethod
    def raid_buffs(cls):
        """returns all raid buffs"""
        return {cls.DIV, cls.TRICK, cls.BROTHERHOOD, cls.TECH, cls.DEVOTION, cls.EMBOLDEN}

    def avg_buff_effect(self, job: Jobs) -> float:
        """
        Calculates effective multiplier that a raid buff contributes to DPS.
        This treats a raid buff as having its effect averaged over the course of a fight and applies that
        average effect to all damage.
        :param job: The job for which the buff is being applied to.
        :return: A multiplier to apply for the whole fight that acts as the buff boost
        """
        if self.name == 'EMBOLDEN':  # pylint: disable=comparison-with-callable
            if job == Jobs.RDM or job.role in {Roles.TANK, Roles.MELEE, Roles.RANGED}:
                decay_interval = 4
                decay_rate = 0.2
                decay_ticks = self.duration_sec // decay_interval
                intervals = (self.multiplier * (1 - decay_rate * tick) * decay_interval / self.cooldown_sec
                             for tick in range(decay_ticks))
                return sum(intervals)
            return 0  # Sucks to not have Embolden apply, I guess
        return self.multiplier * self.duration_sec / self.cooldown_sec


class Jobs(Enum):
    """
    Contains job related info.

    job_mod: The bonus given to the main stat.
    role: The Role of the job
    raidbuff: A list of all raidbuffs that the job has

    job modifiers from https://www.akhmorning.com/allagan-studies/modifiers/
    note: tanks use STR for damage
    """
    SCH = (115, Roles.HEALER, [Buffs.CHAIN])
    AST = (115, Roles.HEALER, [Buffs.DIV])
    WHM = (115, Roles.HEALER, [])
    PLD = (100, Roles.TANK, [])
    WAR = (105, Roles.TANK, [])
    DRK = (105, Roles.TANK, [])
    GNB = (100, Roles.TANK, [])
    NIN = (110, Roles.MELEE, [Buffs.TRICK])
    DRG = (115, Roles.MELEE, [Buffs.LITANY])
    MNK = (110, Roles.MELEE, [Buffs.BROTHERHOOD])
    SAM = (112, Roles.MELEE, [])
    MCH = (115, Roles.RANGED, [])
    DNC = (115, Roles.RANGED, [Buffs.TECH])
    BRD = (115, Roles.RANGED, [Buffs.BV, Buffs.BARD_CRIT, Buffs.BARD_DH])
    SMN = (115, Roles.CASTER, [Buffs.DEVOTION])
    BLM = (115, Roles.CASTER, [])
    RDM = (115, Roles.CASTER, [Buffs.EMBOLDEN])

    def __init__(self, job_mod: int, role: Roles, raidbuff: list[Buffs]):
        self.job_mod = job_mod
        self.role = role
        self.raidbuff = raidbuff


@dataclass(init=False)
class Comp:
    """
    The party composition.

    jobs: A list of all jobs in the party (may contain duplicates).
    raidbuffs: A set of unique raidbuffs in the party.
    n_roles: A number (1-5) indicating how many unique roles are in the party.
    """

    def __init__(self, jobs: list[Jobs]):
        """
        :param jobs: A list of Jobs in the party composition

        jobs: A list of all jobs in the party (may contain duplicates).
        raidbuffs: A set of unique raidbuffs in the party.
        n_roles: A number (1-5) indicating how many unique roles are in the party.
        """

        self.jobs: list[Jobs] = jobs
        self.raidbuffs: set[Buffs] = set(itertools.chain.from_iterable([job.raidbuff for job in jobs]))
        self.n_roles: int = len({job.role for job in jobs})


class CharacterStatFactory:  # pylint: disable=too-few-public-methods
    """
    Takes a String and outputs Job Enum, Mainstat (and Potency calc when available). Raises KeyError.
    """
    @staticmethod
    def create_job(name: str) -> tuple[Jobs, str, ]:
        """
        :param name: The three letter abbreviation of the job in all uppercase as a string.
        :return: A tuple containing the job enum, a string identifying the primary stat, and potency_per_sec calc
        """
        job_string_to_enum = {
            "SCH": (Jobs.SCH, "MND"),
            "AST": (Jobs.AST,),
            "WHM": (Jobs.WHM,),
            "PLD": (Jobs.PLD,),
            "WAR": (Jobs.WAR,),
            "DRK": (Jobs.DRK,),
            "GNB": (Jobs.GNB,),
            "NIN": (Jobs.NIN,),
            "DRG": (Jobs.DRG,),
            "MNK": (Jobs.MNK,),
            "SAM": (Jobs.SAM,),
            "MCH": (Jobs.MCH,),
            "DNC": (Jobs.DNC,),
            "BRD": (Jobs.BRD,),
            "SMN": (Jobs.SMN,),
            "BLM": (Jobs.BLM,),
            "RDM": (Jobs.RDM,),
        }

        return job_string_to_enum[name]

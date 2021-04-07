# Representation of static information at the class level

from enum import Enum, auto
import itertools
import math


class Roles(Enum):
    TANK = auto()
    HEALER = auto()
    MELEE = auto()
    RANGED = auto()
    CASTER = auto()


class Buffs(Enum):
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

    def __init__(self, multiplier, duration, cd):
        self.multiplier = multiplier
        self.duration = duration
        self.cd = cd

    @classmethod
    def crit_buffs(cls):
        return {cls.CHAIN, cls.LITANY, cls.DEVILMENT, cls.BARD_CRIT}

    @classmethod
    def dh_buffs(cls):
        return {cls.BV, cls.BARD_DH, cls.DEVILMENT}

    @classmethod
    def raid_buffs(cls):
        return {cls.DIV, cls.TRICK, cls.BROTHERHOOD, cls.TECH, cls.DEVOTION, cls.EMBOLDEN}

    def avg_buff_effect(self, job):
        total = 0
        if self.name == 'EMBOLDEN':
            if job == Jobs.RDM or job.role in {Roles.TANK, Roles.MELEE, Roles.RANGED}:
                decay_interval = 4
                decay_rate = 0.2
                for i in range(self.duration / decay_interval):
                    total += self.multiplier * (1 - decay_rate * i) * decay_interval / self.cd
                return total
            return 0 # Sucks to not have Embolden apply, I guess
        return self.multiplier * self.duration / self.cd

class Jobs(Enum):
    # job modifiers from https://www.akhmorning.com/allagan-studies/modifiers/
    SCH = (115, Roles.HEALER, [Buffs.CHAIN])
    AST = (115, Roles.HEALER, [Buffs.DIV])
    WHM = (115, Roles.HEALER, [])
    PLD = (110, Roles.TANK, [])
    WAR = (110, Roles.TANK, [])
    DRK = (110, Roles.TANK, [])
    GNB = (110, Roles.TANK, [])
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

    def __init__(self, job_mod, role, raidbuff):
        self.job_mod = job_mod
        self.role = role
        self.raidbuff = raidbuff


class Comp:

    def __init__(self, jobs):
        self.jobs = jobs
        self.raidbuffs = set(itertools.chain.from_iterable([job.raidbuff for job in jobs]))
        self.n_roles = len(set([job.role for job in jobs]))


class JobFactory:
    """
    Takes a String and outputs Job Enum, Mainstat (and Potency calc when available). Raises KeyError.
    """
    @staticmethod
    def create_job(name: str):
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

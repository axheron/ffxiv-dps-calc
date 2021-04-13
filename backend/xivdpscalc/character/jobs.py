""" Representation of static information at the class level """

from enum import Enum, auto
import itertools

class Roles(Enum):
    """ Roles enum """
    TANK = auto()
    HEALER = auto()
    MELEE = auto()
    RANGED = auto()
    CASTER = auto()


class Buffs(Enum):
    """ Buffs enum representing (magnitude, duration, cooldown) in seconds """
    # aoe
    CHAIN = (0.1, 15, 120)
    DIV = (0.06, 15, 120)  # 3 seal div
    TRICK = (0.05, 15, 60)
    LITANY = (0.1, 20, 180)
    BROTHERHOOD = (0.05, 15, 90)
    BV = (0.2, 20, 180)
    BARD_CRIT = (0.02, 30, 80) # Wanderer's Minuet
    BARD_DH = (0.03, 20, 80) # Army's Paeon
    BARD_DMG = (0.01, 30, 80) # Mage's Ballad
    TECH = (0.05, 20, 120)
    DEVOTION = (0.05, 15, 180)
    EMBOLDEN = (0.1, 20, 120)
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
        self.cooldown = cd

    @classmethod
    def crit_buffs(cls):
        """ Lists crit buffs """
        return {cls.CHAIN, cls.LITANY, cls.DEVILMENT, cls.BARD_CRIT}

    @classmethod
    def dh_buffs(cls):
        """ Lists direct hit buffs """
        return {cls.BV, cls.BARD_DH, cls.DEVILMENT}

    @classmethod
    def raid_buffs(cls):
        """ Lists damage buffs """
        return {cls.DIV, cls.TRICK, cls.BROTHERHOOD, cls.BARD_DMG, cls.TECH, cls.DEVOTION, cls.EMBOLDEN}

    def avg_buff_effect(self, job):
        """ Calculates the average impact of buffs considering its uptime and magnitude """
        total = 0
        if self.name == 'EMBOLDEN':  #pylint: disable=comparison-with-callable
            if job == Jobs.RDM or job.role in {Roles.TANK, Roles.MELEE, Roles.RANGED}:
                decay_interval = 4
                decay_rate = 0.2
                for i in range(self.duration / decay_interval):
                    total += self.multiplier * (1 - decay_rate * i) * decay_interval / self.cooldown
                return total
            return 0 # Sucks to not have Embolden apply, I guess
        return self.multiplier * self.duration / self.cooldown

class Jobs(Enum):
    """ Job modifiers from https://www.akhmorning.com/allagan-studies/modifiers/ """
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
    BRD = (115, Roles.RANGED, [Buffs.BV, Buffs.BARD_CRIT, Buffs.BARD_DH, Buffs.BARD_DMG])
    SMN = (115, Roles.CASTER, [Buffs.DEVOTION])
    BLM = (115, Roles.CASTER, [])
    RDM = (115, Roles.CASTER, [Buffs.EMBOLDEN])

    def __init__(self, job_mod, role, raidbuff):
        self.job_mod = job_mod
        self.role = role
        self.raidbuff = raidbuff

    @staticmethod
    def create_job(name: str):
        """
        Takes a String and outputs Job Enum, Mainstat (and Potency calc when available).
        Raises KeyError
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


class Comp:  #pylint: disable=too-few-public-methods
    """ Representation of a comp, basically a collection of Jobs """
    def __init__(self, jobs):
        self.jobs = jobs
        self.raidbuffs = set(itertools.chain.from_iterable([job.raidbuff for job in jobs]))
        self.n_roles = len({job.role for job in jobs})

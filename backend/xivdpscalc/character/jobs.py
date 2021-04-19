""" Representation of static information at the class level """

from enum import Enum, auto
from dataclasses import dataclass
import itertools

class Roles(Enum):
    """ Roles enum """
    TANK = (auto(), 1)
    HEALER = (auto(), 1.3)
    MELEE = (auto(), 1)
    RANGED = (auto(), 1.2)
    CASTER = (auto(), 1.3)

    def __init__(self, enum_id, trait_bonus: float):
        self.enum_id = enum_id
        self.trait_bonus = trait_bonus

class Buffs(Enum):
    """
    List of all buffs in the game. Each buff has three parameters: magnitude, duration, cooldown, in seconds.
    """
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

    def __init__(self, multiplier: float, duration_sec: int, cooldown_sec: int):
        self.multiplier = multiplier
        self.duration_sec = duration_sec
        self.cooldown_sec = cooldown_sec

    @classmethod
    def crit_buffs(cls):
        """ Lists crit buffs """
        return {cls.CHAIN, cls.LITANY, cls.DEVILMENT, cls.BARD_CRIT}

    @classmethod
    def dh_buffs(cls):
        """ Lists direct hit buffs """
        return {cls.BV, cls.BARD_DH, cls.DEVILMENT}

    @classmethod
    def damage_buffs(cls):
        """ Lists damage buffs """
        return {cls.DIV, cls.TRICK, cls.BROTHERHOOD, cls.BARD_DMG, cls.TECH, cls.DEVOTION, cls.EMBOLDEN}

    def avg_buff_effect(self, job):
        """ Calculates the average impact of buffs considering its uptime and magnitude """
        if self.name == 'EMBOLDEN':   # pylint: disable=comparison-with-callable
            if job == Jobs.RDM or job.role in {Roles.TANK, Roles.MELEE, Roles.RANGED}:
                decay_interval = 4
                decay_rate = 0.2
                decay_ticks = self.duration_sec // decay_interval
                intervals = (self.multiplier * (1 - decay_rate * tick) * decay_interval / self.cooldown_sec
                             for tick in range(decay_ticks))
                return sum(intervals)
            return 0 # Sucks to not have Embolden apply, I guess
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
    BRD = (115, Roles.RANGED, [Buffs.BV, Buffs.BARD_CRIT, Buffs.BARD_DH, Buffs.BARD_DMG])
    SMN = (115, Roles.CASTER, [Buffs.DEVOTION])
    BLM = (115, Roles.CASTER, [])
    RDM = (115, Roles.CASTER, [Buffs.EMBOLDEN])

    def __init__(self, job_mod: int, role: Roles, raidbuffs: list[Buffs]):
        self.job_mod = job_mod
        self.role = role
        self.raidbuffs = raidbuffs

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
        self.raidbuffs: set[Buffs] = set(itertools.chain.from_iterable([job.raidbuffs for job in jobs]))
        self.n_roles: int = len({job.role for job in jobs})

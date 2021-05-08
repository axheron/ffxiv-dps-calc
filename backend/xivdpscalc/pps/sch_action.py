""" Sch specific enums for simulation """

from enum import Enum, auto
from xivdpscalc.types import CastTime, ElapsedTime

class SchAction(Enum):
    """
    Enum representing possible sch actions
    """
    BROIL3 = (0, 290, 2.5, True, 2.5)
    RUIN2 = (1, 200, 0, True, 2.5)
    AETHERFLOW = (2, 0, 0, False, 60)
    ENERGYDRAIN = (3, 100, 0, False, 3)
    BIOLYSIS = (4, 0, 0, True, 0)
    DISSIPATION = (5, 0, 0, False, 180)
    SWIFTCAST = (6, 0, 0, False, 60)
    CHAINSTRATAGEM = (7, 0, 0, False, 120)

    def __init__(self, index: int, potency: int, cast_time: CastTime, is_gcd: bool, cooldown: ElapsedTime): # pylint: disable=too-many-arguments
        self.index = index
        self.potency = potency
        self.cast_time = cast_time
        self.is_gcd = is_gcd
        self.cooldown = cooldown

class SchEffect(Enum):
    """
    Enum representing possible active effects that are relevant to scholars
    """
    BIOLYSIS = (True, 70)
    SWIFTCAST = (False, 0)

    def __init__(self, is_dot: bool, potency: int):
        self.is_dot = is_dot
        self.potency = potency

class SchResource(Enum):
    """
    Enum representing possible resource counts that are relevant to scholars
    """
    AETHERFLOW = auto()
    MP = auto()

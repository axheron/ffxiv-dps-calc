"""Contains the formula for calculating damage of a single ability"""
from typing import Optional
from enum import Enum
import math

from xivdpscalc.character import Character
from xivdpscalc.character.jobs import Buffs
from xivdpscalc.character.stat import Stat, Stats

class ProbabilityRolls(Enum):
    """Tuple to hold whether or not damage is a crit/dh/both"""
    IS_CRIT_ONLY = (True, False)
    IS_DH_ONLY = (False, True)
    IS_NORMAL = (False, False)
    IS_CDH = (True, True)

    def __init__(self, is_crit: bool, is_direct_hit: bool):
        self.is_crit = is_crit
        self.is_direct_hit = is_direct_hit

def calc_damage(potency: float, character: Character,
                probability_rolls: ProbabilityRolls, active_buffs: Optional[list[Buffs]] = None,
                is_dot: Optional[bool] = False) -> float:
    """
    Calculates the damage given by a single hit. The equation is given here:
    https://www.akhmorning.com/allagan-studies/how-to-be-a-math-wizard/shadowbringers/damage-and-healing/#damage-dealt
    f(weapon_damage)
    :param potency: potency value of the ability
    :param character: character job, weapon damage, and stats
    :param is_crit: if roll is crit
    :param is_direct_hit: if roll is direct hit
    :param active_buffs: all active buffs at the time of the ability
    :param is_dot: If potency also applies to DoT
    :returns: damage value
    """

    # apply weapon damage
    damage = weapon_damage_factor(potency, character.wd, character.character_stats[Stats.MAINSTAT])

    # applying the damage bonus from secondary stats
    damage = character.character_stats[Stats.DET].apply_stat(damage)
    damage = character.character_stats[Stats.TEN].apply_stat(damage)
    if is_dot:
        damage = character.character_stats[Stats.SPEED].apply_stat(damage)

    damage //= 100  # why? i do not know. cargo culted

    # trait bonus
    damage = math.floor(character.job.role.trait_bonus * damage)

    # damage effect of probabalistic stats
    if probability_rolls.is_crit and not probability_rolls.is_direct_hit:
        damage = character.character_stats[Stats.CRIT].apply_stat(damage)
    if probability_rolls.is_direct_hit and not probability_rolls.is_crit:
        damage = damage * character.character_stats[Stats.DH].stat.m_factor // 1000
    if probability_rolls.is_crit and probability_rolls.is_direct_hit:
        crit_damage = character.character_stats[Stats.CRIT].apply_stat(damage)
        damage = crit_damage * character.character_stats[Stats.DH].stat.m_factor // 1000

    # apply raid buffs that boost damage
    if active_buffs is not None:
        for buff in active_buffs:
            if buff in Buffs.damage_buffs():
                damage *= (1 + buff.avg_buff_effect(character.job))

    return damage

def weapon_damage_factor(potency: int, weapon_damage: int, mainstat: Stat) -> int:
    """
    Returns the effect of weapon damage on the damage number
    :param potency: potency of the ability
    :param weapon_damage: character weapon damage
    :param mainstat: main stat value of the character
    :return: the amount of damage contributed by weapon damage
    """
    return potency * weapon_damage * (100 + mainstat.get_multiplier()) // 100

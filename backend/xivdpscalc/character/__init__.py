""" Representation of a single character and its stat spread """

import math
from typing import Optional
from dataclasses import dataclass
from xivdpscalc.character.stat import Stat, Stats, ProbabalisticStat
from xivdpscalc.character.jobs import Roles, Buffs, Comp, Jobs

@dataclass
class CharacterStatSpread:  # pylint: disable=too-many-instance-attributes
    """
    Value class representation of a stat spread
    """
    wd: float
    mainstat: int
    det: int
    crit: int
    dh: int
    speed: int
    ten: int
    pie: int

class Character:
    """
    The main class where damage is calculated. Initialized by providing a CharacterStatSpread.
    """
    def __init__(self, job: Jobs, stat_spread: CharacterStatSpread):
        """
        :param job: Job enum, tells the character's job
        :param stat_spread: dataclass containing all the attributes
        """
        self.job = job
        self.wd = stat_spread.wd
        self.character_stats = {
            Stats.MAINSTAT: Stat(Stats.MAINSTAT, stat_spread.mainstat),
            Stats.DET: Stat(Stats.DET, stat_spread.det),
            Stats.CRIT: ProbabalisticStat(Stats.CRIT, stat_spread.crit),
            Stats.DH: ProbabalisticStat(Stats.DH, stat_spread.dh),
            Stats.SPEED: Stat(Stats.SPEED, stat_spread.speed),
            Stats.TEN: Stat(Stats.TEN, stat_spread.ten),
            Stats.PIE: Stat(Stats.PIE, stat_spread.pie),
        }

    def get_gcd(self) -> float:
        """
        Returns the character's gcd given its skill or spell speed
        :returns: the gcd in seconds
        """
        return math.floor(0.25 * (1000 - self.character_stats[Stats.SPEED].get_multiplier())) / 100

    def get_dot_scalar(self) -> float:
        """
        Returns the character's dot damage bonus, given its skill or spell speed
        :returns: the modified dot multiplier
        """
        return 1 + (self.character_stats[Stats.SPEED].get_multiplier() / 1000)

    def calc_piety(self) -> float:
        """
        Returns the character's mp regen resulting from the piety stat
        :returns: The character's mp regen per tick (3 seconds)
        """
        return 200 + self.character_stats[Stats.PIE].get_multiplier()

    # todo: break this up neatly
    def calc_damage(self, potency_per_second: float, comp: Comp, is_dot: bool = False,
                    crit_rate: Optional[float] = None, dh_rate: Optional[float] = None) -> float:  #pylint: disable=too-many-arguments, too-many-locals
        """
        Calculates the damage from non probablistic stats.
        :param potency_per_second: From potency calculated on expected rotation
        :param comp: Team composition, if applicable
        :param is_dot: If potency also applies to DoT
        :returns: DPS contribution from non-probablistic stats
        """

        # modify mainstat according to number of roles if with a team composition
        if comp is not None:
            affirmative_action_bonus = 1 + 0.01 * comp.n_roles
            new_mainstat_value = math.floor(self.character_stats[Stats.MAINSTAT].value * affirmative_action_bonus)
            mainstat = Stat(Stats.MAINSTAT, new_mainstat_value)
        else:
            mainstat = self.character_stats[Stats.MAINSTAT]

        # job bonus for weapon damage
        adjusted_wd = self.wd + (340 * self.job.job_mod // 1000)
        np_damage = potency_per_second * adjusted_wd * (100 + mainstat.get_multiplier()) // 100

        # applying the damage bonus from wimpy secondary stats
        np_damage = self.character_stats[Stats.DET].apply_stat(np_damage)
        np_damage = self.character_stats[Stats.TEN].apply_stat(np_damage)
        if is_dot:
            np_damage = self.character_stats[Stats.SPEED].apply_stat(np_damage)

        return np_damage

    def calc_probablistic_damage(self, np_damage: float, comp: Comp = None, crit_rate: float = None,
                                 dh_rate: float = None) -> float:
        """
        Calculates the damage from probablistic stats.
        :param np_damage: from nonprobablistic damage calculation
        :param comp: Team composition, if applicable
        :param crit_rate: for calculating a specific crit proc rate
        :param dh_rate: for calculating a specific dh proc rate
        :returns: DPS contribution from probablistic stats
        """

        # damage effect of probabalistic stats
        crit_damage = self.character_stats[Stats.CRIT].apply_stat(np_damage)
        dh_damage = np_damage * self.character_stats[Stats.DH].stat.m_factor // 1000
        cdh_damage = crit_damage * self.character_stats[Stats.DH].stat.m_factor // 1000

        # use expected crit rate based on stats if none is supplied
        if crit_rate is None:
            crit_rate = self.character_stats[Stats.CRIT].get_p()
        if dh_rate is None:
            dh_rate = self.character_stats[Stats.DH].get_p()

        # apply party crit/dh buffs if applicable
        if comp is not None:
            for buff in comp.raidbuffs:
                if buff in Buffs.crit_buffs():
                    crit_rate += buff.avg_buff_effect(self.job)
                elif buff in Buffs.dh_buffs():
                    dh_rate += buff.avg_buff_effect(self.job)

        # apply probablistic modifiers
        assert crit_rate is not None  # for mypy
        assert dh_rate is not None  # for mypy
        cdh_rate = crit_rate * dh_rate
        normal_rate = 1 - crit_rate - dh_rate + cdh_rate
        p_damage = np_damage * normal_rate + (
            crit_damage * (crit_rate - cdh_rate)) + (
            dh_damage * (dh_rate - cdh_rate)) + (
            cdh_damage * cdh_rate)

        return p_damage

    # todo: break this up neatly
    def calc_damage(self, potency_per_second: float, comp: Comp = None,  # pylint: disable=too-many-arguments
                    is_dot: bool = False, crit_rate: float = None, dh_rate: float = None) -> float:
        """
        Calculates the estimated DPS based on the team composition and current character stats
        :param potency_per_second: Potency calculated on expected rotation
        :param comp: Team composition
        :param is_dot: The potency is applying to a DoT effect, which is additionally modified by spellspeed
        :param crit_rate: Optional parameter to override crit rate to calculate specific proc rate
        :param dh_rate: Optional parameter to override dh rate to calculate specific proc rate
        :returns: the DPS number
        """
        damage = self.calc_non_probablistic_damage(potency_per_second, comp, is_dot)
        damage //= 100  # why? i do not know. cargo culted

        # damage effect of job traits / stance
        # todo: pull out traits
        if self.job.role == Roles.HEALER:
            damage = math.floor(damage * 1.3)  # magic and mend

        total_damage = self.calc_probablistic_damage(damage, comp, crit_rate, dh_rate)

        # apply raid buffs that boost damage
        if comp is not None:
            for buff in comp.raidbuffs:
                if buff in Buffs.damage_buffs():
                    total_damage *= (1 + buff.avg_buff_effect(self.job))

        return total_damage

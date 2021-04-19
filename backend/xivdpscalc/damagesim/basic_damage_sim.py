"""
calculates damage by using pps instead of raw potency and time values and averaging out the effect of buffs
"""
from typing import NamedTuple
import math

from xivdpscalc.character import Character
from xivdpscalc.character.stat import Stat, Stats
from xivdpscalc.character.jobs import Buffs, Comp
from xivdpscalc.damagesim.damage_formula import calc_damage, ProbabilityRolls

class ProbabilityRates(NamedTuple):
    """
    Stores the probability rates used to calculate dps
    """
    cdh_rate: float
    crit_only_rate: float
    dh_only_rate: float
    normal_rate: float

class BasicDamageSim:
    """This is a damage simulation that uses potency per second and averages the effect of buffs over time. It does not
    consider buffs/and specific potency timing.

    :param potency_per_second: average potency over the fight
    :param character: Character class containing stats and job of calculation
    :param team_comp: Optional, contains a comp class that has buffs and unique roles
    :param crit_override: Optional parameter to override the crit rate
    :param dh_override: Optional parameter to override the dh rate
    """

    def __init__(self, character: Character, potency_per_second: float,
                 team_comp: Comp = None, crit_override: float = None, dh_override: float = None):
        """Constructor method
        """
        self.potency_per_second = potency_per_second
        self.character = character
        self.team_comp = team_comp
        self._modify_weapondamage()
        if team_comp is not None:
            self._unique_role_bonus()
        self._init_probability_rates(crit_override, dh_override)

    def _init_probability_rates(self, crit_override: float, dh_override: float):
        """
        Private method to calculate the probability rates to determine which calculation to run
        :param crit_override: Optional parameter to override the crit rate
        :param dh_override: Optional parameter to override the dh rate
        """
        crit_rate, dh_rate = self._calculate_probability_stats()
        if crit_override is not None:
            crit_rate = crit_override
        if dh_override is not None:
            dh_rate = dh_override
        cdh_rate = crit_rate * dh_rate
        normal_rate = 1 - crit_rate - dh_rate + cdh_rate
        crit_only_rate = crit_rate - cdh_rate
        dh_only_rate = dh_rate - cdh_rate
        self.probabilty_rate = ProbabilityRates(cdh_rate, crit_only_rate, dh_only_rate, normal_rate)

    def _unique_role_bonus(self):
        """
        Modify mainstat according to number of roles if with a team composition
        """
        unique_role_bonus = 1 + 0.01 * self.team_comp.n_roles
        new_mainstat_value = math.floor(self.character.character_stats[Stats.MAINSTAT].value * unique_role_bonus)
        self.character.character_stats[Stats.MAINSTAT] = Stat(Stats.MAINSTAT, new_mainstat_value)

    def _modify_weapondamage(self):
        """
        modify weapon damage with job modifier
        """
        self.character.wd += (340 * self.character.job.job_mod // 1000)

    def _calculate_probability_stats(self) -> (float, float):
        """
        Calculates the pure crit and dh rate.
        :return: a tuple containing crit rate, dh rate
        """
        crit_rate = self.character.character_stats[Stats.CRIT].get_p()
        dh_rate = self.character.character_stats[Stats.DH].get_p()
        for buff in self.team_comp.raidbuffs:
            if buff in Buffs.crit_buffs():
                crit_rate += buff.avg_buff_effect(self.character.job)
            elif buff in Buffs.dh_buffs():
                dh_rate += buff.avg_buff_effect(self.character.job)
        return (crit_rate, dh_rate)

    def calc_dps(self) -> float:
        """
        Calculates the dps using a basic model with time averaged buffs.
        :return: The dps as a floating point number.
        """

        damage = sum([
            self.probabilty_rate.normal_rate * calc_damage(self.potency_per_second, self.character, ProbabilityRolls.IS_NORMAL),
            self.probabilty_rate.crit_only_rate * calc_damage(self.potency_per_second, self.character, ProbabilityRolls.IS_CRIT_ONLY),
            self.probabilty_rate.dh_only_rate * calc_damage(self.potency_per_second, self.character, ProbabilityRolls.IS_DH_ONLY),
            self.probabilty_rate.cdh_rate * calc_damage(self.potency_per_second, self.character, ProbabilityRolls.IS_CDH),
        ])
        # apply raid buffs that boost damage
        if self.team_comp is not None:
            for buff in self.team_comp.raidbuffs:
                if buff in Buffs.damage_buffs():
                    damage *= (1 + buff.avg_buff_effect(self.character.job))

        return damage

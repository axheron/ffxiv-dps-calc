""" Sch specific implementation of pps calculation """

import math

from xivdpscalc.pps import HealerPps

class SchPps(HealerPps):
    """ Sch specific implementation of pps and mpps calculations.
    Currently only has direct ports from the spreadsheet """
    r2_potency = 200
    b3_potency = 290
    bio_potency = 70
    ed_potency = 100

    def get_pps(self, character_stats, caster_tax=0.1, num_ed_per_min=4, num_filler_casts=0):
        """
        Get the expected PPS.
        A port of the sch spreadsheet's pps function.
        """
        return self.total_potency_spreadsheet_port(
            character_stats, caster_tax, num_ed_per_min, num_filler_casts) / self.get_cycle(
                character_stats, caster_tax)

    def get_mp_per_min(self, character_stats, caster_tax=0.1, succ=0, adlo=0, ed=4, rez=0):
        """
        Get the expected mp consumption in a minute.
        """
        cycle = self.get_cycle(character_stats, caster_tax)
        mpps = self.mp_consumed_per_cycle(
            character_stats, caster_tax, succ, adlo, ed, rez, cycle) / cycle
        return 20 * character_stats.calc_piety() - 60 * mpps

    def total_potency_spreadsheet_port(self, character_stats, caster_tax, ed_per_min, num_filler):
        """
        Get the total potency in get_cycle() seconds.
        A direct port of getP in the sch spreadsheet.
        """
        # do as the spreadsheet do
        short_gcd = character_stats.get_gcd()

        result = 0
        result += 3 * self.ed_potency * ed_per_min

        sps_scalar = character_stats.get_dot_scalar()
        # 1 bio + x B3 and 4 R2s that replace B3s
        # First see if our gcd is short enough to make gcd counts weird
        if ((30 - 2 * short_gcd) % (short_gcd + caster_tax)) > 1.5:
            # split the 180s window into 6 30 second windows,
            # calculate the number of b3s (minus one bio and one r2 or swift b3 per window)
            # Adds the potencies of 2 swift broils plus 4 r2s to this
            result += 6 * math.ceil(
                (30 - 2 * short_gcd) / (short_gcd + caster_tax)) * self.b3_potency
            result += 2 * self.b3_potency + 4 * self.r2_potency
            # apply bio potency
            result += 6 * 10 * sps_scalar * self.bio_potency
        else:
            result += 6 * math.floor(
                (30 - 2 * short_gcd) / (short_gcd + caster_tax)) * self.b3_potency
            result += 2 * self.b3_potency + 4 * self.r2_potency

            result += 6 * 9 * sps_scalar * self.bio_potency
            result += 6 * (
                (3 - ((30 - 2 * short_gcd) % (short_gcd + caster_tax))) / 3)  \
                * sps_scalar * self.bio_potency

        result -= 3 * num_filler * self.b3_potency

        return result

    @classmethod
    def get_cycle(cls, character_stats, caster_tax):
        """
        Actual time taken by a 180s rotation, is lower than 180s
        """
        short_gcd = character_stats.get_gcd()
        result = 0
        # 1 bio + x Broils and 4 R2s/3min
        if (30 - 2 * short_gcd) % (short_gcd + caster_tax) > 1.5 :
            result += 6 * (
                2 * short_gcd + math.ceil((30 - 2 * short_gcd) /
                    (short_gcd + caster_tax)) * (short_gcd + caster_tax)) - 1 * caster_tax
        else:
            result += 6 * (
                2 * short_gcd+math.floor((30 - 2 * short_gcd) /
                    (short_gcd + caster_tax)) * (short_gcd + caster_tax)) - 1 * caster_tax
        return result

    @classmethod
    def mp_consumed_per_cycle(cls, character_stats, caster_tax, succ, adlo, ed, rez, cycle):
        """MP consumed over a 3 min cycle (positive = losing mp, negative = gaining mp)"""
        short_gcd = character_stats.get_gcd()
        result = 0
        if (30 - 2 * short_gcd) % (short_gcd + caster_tax) > 1.5:
            result += 6 * math.ceil(2 + (30 - 2 * short_gcd) / (short_gcd + caster_tax)) * 400
        else:
            result += 6 * math.floor(2 + (30 - 2 * short_gcd) / (short_gcd + caster_tax)) * 400

        result += 700 * succ * cycle / 60
        result += 600 * adlo * cycle / 60
        result += 2000 * rez * cycle / 60
        # Aetherflow
        result -= 1000 * cycle / 60
        # Lucid
        result -= 3500 * cycle / 60
        # Energy Drain
        result -= 500 * ed * cycle / 60
        return result

    # TODO: it wasn't implement in Pps or HealerPps, so clearly it needs to be implemented at
    # some level of inheritance
    def calculate_pps(self, character_stats, caster_tax):
        """
        # hard coded for a ~180 second cycle, actual length calculated by get_cycle
        # character_stats is a backend.character.Character object
        # todo: extend this for variable length
        """
        ...

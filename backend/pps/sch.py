import math

from calc import CharacterStats
from pps.pps import HealerPps


class SchPps(HealerPps):
    r2_potency = 200
    b3_potency = 290
    bio_potency = 70
    ed_potency = 100
        
    def get_pps(self, character_stats, caster_tax=0.1, num_ed_per_min=4, num_filler_casts=0):
        return self.total_potency_spreadsheet_port(character_stats, caster_tax, num_ed_per_min, num_filler_casts) / self.get_cycle(character_stats, caster_tax)

    def get_mp_per_min(self, character_stats, caster_tax=0.1, succ=0, adlo=0, ed=4, rez=0):
        cycle = self.get_cycle(character_stats, caster_tax)
        mpps = self.mp_consumed_per_cycle(character_stats, caster_tax, succ, adlo, ed, rez, cycle) / cycle
        return 20 * character_stats.calc_piety() - 60 * mpps 
        
    # hard coded for a ~180 second cycle, actual length calculated by get_cycle
    # todo: extend this for variable length
    def total_potency_spreadsheet_port(self, character_stats, caster_tax, ed_per_min, num_filler_casts):
        # do as the spreadsheet do        
        short_gcd = character_stats.get_gcd()
        
        result = 0
        result += 3 * self.ed_potency * ed_per_min
        
        sps_scalar = character_stats.get_dot_scalar()
        # 1 bio + x B3 and 4 R2s that replace B3s
        if (((30 - 2 * short_gcd) % (short_gcd + caster_tax)) > 1.5):
            result += 6 * math.ceil((30 - 2 * short_gcd) / (short_gcd + caster_tax)) * self.b3_potency + 2 * self.b3_potency + 4 * self.r2_potency
            result += 6 * 10 * sps_scalar * self.bio_potency
        else:
            result += 6 * math.floor((30 - 2 * short_gcd) / (short_gcd + caster_tax)) * self.b3_potency + 2 * self.b3_potency + 4 * self.r2_potency
            
            result += 6 * 9 * sps_scalar * self.bio_potency
            result += 6 * ((3 - ((30 - 2 * short_gcd) % (short_gcd + caster_tax))) / 3) * sps_scalar * self.bio_potency
            
        result -= 3 * num_filler_casts * self.b3_potency
                
        return result
        
    # Actual time taken by a 180s rotation, is lower than 180s
    def get_cycle(self, character_stats, caster_tax):
        short_gcd = character_stats.get_gcd()
        result = 0
        # 1 bio + x Broils and 4 R2s/3min
        if ((30 - 2 * short_gcd) % (short_gcd + caster_tax) > 1.5) : 
            result += 6 * (2 * short_gcd + math.ceil((30 - 2 * short_gcd) / (short_gcd + caster_tax)) * (short_gcd + caster_tax)) - 1 * caster_tax
        else:  
            result += 6 * (2 * short_gcd+math.floor((30 - 2 * short_gcd) / (short_gcd + caster_tax)) * (short_gcd + caster_tax)) - 1 * caster_tax
        return result

    def mp_consumed_per_cycle(self, character_stats, caster_tax, succ, adlo, ed, rez, cycle):
        """MP consumed over a 3 min cycle (positive = losing mp, negative = gaining mp)"""
        short_gcd = character_stats.get_gcd()
        result = 0
        if ((30 - 2 * short_gcd) % (short_gcd + caster_tax) > 1.5):
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

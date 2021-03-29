import math

from backend.calc import CharacterStats
from backend.pps.pps import HealerPps


class SchPps(HealerPps):
    r2_potency = 200
    b3_potency = 290
    bio_potency = 70
    ed_potency = 100
        
    def get_pps(self, character_stats, caster_tax):
        return self.total_potency_spreadsheet_port(character_stats, caster_tax) / self.get_cycle(caster_tax)
        
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
            result += 6 * (2 * short_gcd+math.floor((30-2*short_gcd) / (short_gcd+caster_tax)) * (short_gcd+caster_tax)) - 1 * caster_tax
        return result

import math

from backend.calc import CharacterStats
from backend.pps.pps import HealerPps


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


    
    def get_total_potency_flexible_time(self, character, num_seconds, caster_tax):        
        # At a high level, we take the full window, figure out how many EDs we expect to be able to cast
        #    3 every 60s
        #    3 more every 180s
        #    As long as the final minute is over 9 seconds (or 18 in a dissipation minute), we have no reason to believe any would be wasted
        #        Because I am lazy, I just write off all of the EDs in the last minute as a loss if you don't have time to burn all of them
        #        todo: model partial spending if the last minute is sub 20 seconds
        #    todo: model partial ED usage (ed_per_min or non_ed_per_min or w/e)
        num_af = 3 * math.ceil((num_seconds - 10) / 60) + 3 * math.ceil((num_seconds - 20) / 180) 
        
        # The number of r2s is modeled as:
        #    1 every 120s for chain stratagem unless:
        #    3 every 180s for dissipation (overlaps with chain stratagem r2)
        num_r2 = math.ceil(num_seconds / 120) + 3 * math.ceil(num_seconds / 180) - math.ceil(num_seconds / 360)
        
        # The number of bios is modeled as:
        #    2 every 60s
        num_bio = math.ceil(num_seconds / 30)
        
        # The number of swifted b3s is modeled as:
        #    1 every 60s
        #    unless the last minute is under 30 seconds (losing the second bio)
        #        in which case you lose one (assuming swift is used at the second bio of every minute)
        num_swift_b3 = 1 if num_seconds <= 30 else math.floor(num_bio / 2)
        
        b3_time_budget = (num_seconds - character.get_gcd() * (num_r2 + num_swift_b3 + num_bio))
        num_b3 = math.floor(b3_time_budget / (character.get_gcd() + caster_tax))
        
        # The number of bio ticks is modeled as:
        # 1 tick every 3 seconds, starting on the third second
        #     No partial credit because that's not a thing
        num_bio_ticks = math.floor(num_seconds / 3)
        
        return self.b3_potency * num_b3 + num_r2 * (self.r2_potency) + num_swift_b3 * (self.b3_potency) + self.bio_potency * character.get_dot_scalar() * num_bio_ticks + self.ed_potency * num_af

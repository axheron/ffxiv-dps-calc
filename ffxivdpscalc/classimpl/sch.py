import math

from ffxivdpscalc.calc import CharacterStats


class SchCharacterStats(CharacterStats):
    r2_potency = 200
    b3_potency = 290
    bio_potency = 70
    ed_potency = 100

    def __init__(self, job, wd, mainstat, det, crit, dh, speed, ten, pie):
        super().__init__(job, wd, mainstat, det, crit, dh, speed, ten, pie)
        
    # hard coded for a ~180 second cycle, actual length calculated by get_cycle
    # todo: extend this for variable length, make this less...this
    def pps_spreadsheet_port(self, caster_tax, num_ed_per_min):
        # do as the spreadsheet do        
        short_gcd = self.get_gcd()
        
        result = 0
        result += 3*self.ed_potency*num_ed_per_min
        
        sps_scalar = ((1000+math.floor(130*(self.speed.value-380)/3300))/1000)
        # 1 bio + x B3 and 4 R2s that replace B3s
        if (((30-2*short_gcd) % (short_gcd+caster_tax)) > 1.5):
            result += 6*(math.ceil((30-2*short_gcd)/(short_gcd+caster_tax)))*self.b3_potency+2*self.b3_potency+4*self.r2_potency
            result += 6*10*sps_scalar*self.bio_potency
        else:
            result += 6*(math.floor((30-2*short_gcd)/(short_gcd+caster_tax)))*self.b3_potency+2*self.b3_potency+4*self.r2_potency
            
            result += 6*9*sps_scalar*self.bio_potency
            result += 6*((3-((30-2*short_gcd) % (short_gcd+caster_tax)))/3)*sps_scalar*self.bio_potency
                
        return  result
        
    # Actual time taken by a 180s rotation, I hate this function, so much
    def get_cycle(self, caster_tax):
        short_gcd = self.get_gcd()
        result = 0
        # 1 bio + x Broils and 4 R2s/3min
        if ((30-2*short_gcd) % (short_gcd+caster_tax) > 1.5) : 
            result += 6*(2*short_gcd+math.ceil((30-2*short_gcd)/(short_gcd+caster_tax))*(short_gcd+caster_tax))-1*caster_tax
        else:  
            result += 6*(2*short_gcd+math.floor((30-2*short_gcd)/(short_gcd+caster_tax))*(short_gcd+caster_tax))-1*caster_tax
        return result
    
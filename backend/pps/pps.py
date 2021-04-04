import math

from calc import CharacterStats


class Pps:
        
    # hard coded for a ~180 second cycle, actual length calculated by get_cycle
    # character_stats is a calc.CharacterStats object
    # todo: extend this for variable length
    def calculate_pps(self, character_stats, caster_tax):
        raise NotImplementedError
        
        
class HealerPps(Pps):
    def calculate_pps(self, character_stats, caster_tax):
        raise NotImplementedError

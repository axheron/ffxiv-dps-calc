''' General PPS calculation interfaces '''

class Pps:
    ''' Top level PPS calculation interface. '''
    def calculate_pps(self, character_stats, caster_tax):
        '''
        # hard coded for a ~180 second cycle, actual length calculated by get_cycle
        # character_stats is a backend.character.Character object
        # todo: extend this for variable length
        '''
        raise NotImplementedError

class HealerPps(Pps):
    ''' PPS interface geared specifically for healers '''
    def calculate_pps(self, character_stats, caster_tax):
        '''
        # hard coded for a ~180 second cycle, actual length calculated by get_cycle
        # character_stats is a backend.character.Character object
        # todo: extend this for variable length
        '''
        raise NotImplementedError

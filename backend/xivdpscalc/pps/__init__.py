""" General PPS calculation interfaces """
from abc import ABCMeta, abstractmethod

class Pps(metaclass=ABCMeta):
    """ Top level PPS calculation interface. """

    @abstractmethod
    def calculate_pps(self, character_stats, caster_tax):
        """
        # hard coded for a ~180 second cycle, actual length calculated by get_cycle
        # character_stats is a backend.character.Character object
        # todo: extend this for variable length
        """
        ...

class HealerPps(Pps):
    """ PPS interface geared specifically for healers """

    def calculate_pps(self, character_stats, caster_tax):
        """
        # hard coded for a ~180 second cycle, actual length calculated by get_cycle
        # character_stats is a backend.character.Character object
        # todo: extend this for variable length
        """
        raise NotImplementedError

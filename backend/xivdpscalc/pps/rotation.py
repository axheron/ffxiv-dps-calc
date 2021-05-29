""" High level interface representing rotations to be used by simulators """
from abc import ABCMeta, abstractmethod
from xivdpscalc.types import ElapsedTime
from xivdpscalc.pps.sch_action import SchAction, SchEffect, SchResource

class SchRotation(metaclass=ABCMeta):
    """
    A high level class representing a rotation that is invoked by simulators to get actions.
    """

    @abstractmethod
    def get_action(self, current_time: ElapsedTime, cooldowns: dict[SchAction, float],
                   remaining_effect_durations: dict[SchEffect, float], resources: dict[SchResource, int], gcd: ElapsedTime, ping: ElapsedTime) -> SchAction:
        """
        Calculates the estimated DPS based on the team composition and current character stats
        :param current_time: The time that has passed since the beginning of the simulation
        :param cooldowns: Cooldowns of various actions (including gcds)  0 or negative if the action is available
        :param remaining_effect_durations: The remaining time of timer-based effects.  0 or negative if the effect is inactive
        :param resources: Resource counts, such as MP or Aetherflow
        :returns: the action to be used
        """

""" Sample implementations of scholar rotations """

from xivdpscalc.pps.rotation import SchRotation
from xivdpscalc.pps.sch_action import SchAction, SchEffect, SchResource
from xivdpscalc.types import ElapsedTime

class FixedSchRotation(SchRotation): #pylint: disable=too-few-public-methods
    """
    A Rotation that returns actions in a set order and uses a default action once it iterates through
    """

    def __init__(self, rotation: list[SchAction], default_action: SchAction):
        self.rotation = rotation
        self.index = 0
        self.default_action = default_action

    def get_action(self, current_time: ElapsedTime, cooldowns: dict[SchAction, float],
                   remaining_effect_durations: dict[SchEffect, float], resources: dict[SchResource, int]) -> SchAction:
        """
        Returns a SchAction based on the fixed rotation
        """
        if self.index < len(self.rotation):
            self.index += 1
            return self.rotation[self.index - 1]
        return self.default_action

class SampleSchRotation(SchRotation): #pylint: disable=too-few-public-methods
    """
    An example rotation exibiting more dynamic decision rotation generation.
    This is not meant to be a perfect replication of a good sch rotation, this is primarily for testing and demonstration.
    This operates by starting with a gcd 4 chain opener, and then using a rudimentary priority list to pick actions.
    """

    def __init__(self):
        self.rotation = [SchAction.BIOLYSIS, SchAction.AETHERFLOW, SchAction.ENERGYDRAIN,
                         SchAction.BROIL3, SchAction.BROIL3, SchAction.RUIN2, SchAction.CHAINSTRATAGEM, SchAction.ENERGYDRAIN,
                         SchAction.BROIL3, SchAction.RUIN2, SchAction.ENERGYDRAIN, SchAction.SWIFTCAST, SchAction.BROIL3,
                         SchAction.DISSIPATION, SchAction.ENERGYDRAIN, SchAction.BROIL3, SchAction.RUIN2, SchAction.ENERGYDRAIN]
        self.index = 0

    def get_action(self, current_time: ElapsedTime, cooldowns: dict[SchAction, float],
                   remaining_effect_durations: dict[SchEffect, float], resources: dict[SchResource, int]) -> SchAction:
        """
        Returns a SchAction based on an arbitrary set of rules.
        """
        # broil by default
        selected_action = SchAction.BROIL3
        if self.index < len(self.rotation):
            self.index += 1
            selected_action = self.rotation[self.index - 1]
        elif cooldowns[SchAction.BROIL3] >= 0.75:
            # this is a weaving window
            # the highest cooldown we can have without clipping assuming anim lock of 0.75 seconds
            
            # an dict of each ogcd with its usage constraint, ordered by priority
            ogcd_constraints = {
                SchAction.ENERGYDRAIN: resources[SchResource.AETHERFLOW] > 0, 
                SchAction.CHAINSTRATAGEM: True,
                SchAction.AETHERFLOW: resources[SchResource.AETHERFLOW] <= 0,
                SchAction.DISSIPATION: resources[SchResource.AETHERFLOW] <= 0,
                SchAction.SWIFTCAST: True}
            
            earliest_nonclip_cast_time = cooldowns[SchAction.BROIL3] - 0.75
            # if we can afford it and avoid clipping, ED
            for action in ogcd_constraints:
                if cooldowns[action] <= earliest_nonclip_cast_time and ogcd_constraints[action]:
                    selected_action = action
                    break;
        # if bio needs refreshing
        elif remaining_effect_durations[SchEffect.BIOLYSIS] <= 0:
            selected_action = SchAction.BIOLYSIS
        # if chain stratagem, dissipation, or aetherflow are about to come up, but bio is still up, open a weaving window with r2
        elif cooldowns[SchAction.CHAINSTRATAGEM] < 1.5 or \
            ((cooldowns[SchAction.DISSIPATION] < 1.5) and resources[SchResource.AETHERFLOW] <= 1):
            selected_action = SchAction.RUIN2
        # if aetherflow or dissipation are coming up, we still have aetherflow reserves, and energy drain is up, r2 to ed
        elif (cooldowns[SchAction.AETHERFLOW] < 30 or cooldowns[SchAction.DISSIPATION] < 30) and \
            resources[SchResource.AETHERFLOW] > 1 and \
            cooldowns[SchAction.ENERGYDRAIN] <= 0:
            selected_action = SchAction.RUIN2
        
        return selected_action

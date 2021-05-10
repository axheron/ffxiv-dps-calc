""" Sch specific implementation of pps calculation """

import math

from collections import defaultdict
from xivdpscalc.character import Character
from xivdpscalc.pps import HealerPps
from xivdpscalc.pps.sch_action import SchAction, SchEffect, SchResource, SchSimNotice
from xivdpscalc.types import ElapsedTime
from xivdpscalc.pps.rotation import SchRotation

SchSimTimeline = dict[SchAction, list]

class SchSimResults:
    """ Value class representing results of a dps simulation """
    def __init__(self, timeline: SchSimTimeline, notices: set(SchSimNotice)):
        self.timeline = timeline
        self.notices = notices

    def get_non_dot_potency(self):
        """ Aggregate results to find total non-dot potency """
        total = 0
        for action in SchAction:
            total += len(self.timeline[action]) * action.potency
        return total

class SchPps(HealerPps):
    """ Sch specific implementation of pps and mpps calculations.
    Currently only has direct ports from the spreadsheet """
    r2_potency = 200
    b3_potency = 290
    bio_potency = 70
    ed_potency = 100

    def get_total_potency_variable_time(self, sim_length: ElapsedTime, character_stats: Character, rotation: SchRotation, caster_tax: float = 0.1, ping: ElapsedTime = 0) -> SchSimResults: # pylint: disable=too-many-arguments, too-many-locals
        """
        Get the total potency in sim_length seconds
        rotation is a SchRotation object
        todo: support dot damage calculation (will be implemented in a separate method
        todo: how long is animation lock actually?  Hard coded here for 0.75, have no idea if that's true
        There are some nuances to how this works:
            At present, this sim does not calculate dot damage
            If an action with an active cooldown is selected, the time jumps forward to the cooldown's expiry
            This simulator does not enforce resource requirements - ED can be used even with no aetherflow
        """
        # approximate animation lock is on average 600 ms + average 40 ms server latency + ping
        animation_lock = 0.64 + ping

        timeline: SchSimTimeline = defaultdict(lambda: [])
        notices: set(SchSimNotice) = set()
        current_time: ElapsedTime = 0

        short_gcd = character_stats.get_gcd()

        next_active: defaultdict[SchAction, ElapsedTime] = defaultdict(lambda: 0)
        active_effects: defaultdict[SchEffect, ElapsedTime] = defaultdict(lambda: -1)
        resources: defaultdict[SchResource, int] = defaultdict(lambda: 0)

        while current_time <= sim_length:
            # get the selected action
            selected_action = rotation.get_action(current_time,
                                                  {key: next_active[key] - current_time for key in SchAction},
                                                  {key: active_effects[key] - current_time for key in active_effects},
                                                  resources, short_gcd, ping)

            # find the actual cast time of the selected action (not including caster tax)
            cast_time = character_stats.get_cast_time(selected_action.cast_time)

            # if swiftcast is up and this is a casted spell, eat swiftcast and reduce the cast time to 0
            if active_effects[SchEffect.SWIFTCAST] > current_time and cast_time > 0:
                active_effects[SchEffect.SWIFTCAST] = -1
                cast_time = 0

            # advance the time to when the action is actually available
            current_time = max(current_time, next_active[selected_action])

            # clip the cast if the sim ends before then
            if current_time + cast_time <= sim_length:
                timeline[selected_action].append(current_time)

            # apply cooldowns
            if selected_action.is_gcd:
                for action in SchAction:
                    if action.is_gcd:
                        next_active[action] = current_time + short_gcd
                # For Sch specifically, this is invariably equal to short_gcd, but sonic break exists
                next_active[selected_action] = current_time + character_stats.get_cast_time(selected_action.cooldown)
            else:
                next_active[selected_action] = current_time + selected_action.cooldown

            # apply resource and effect timers as needed
            if selected_action in [SchAction.AETHERFLOW, SchAction.DISSIPATION]:
                resources[SchResource.AETHERFLOW] = 3
            elif selected_action == SchAction.ENERGYDRAIN:
                resources[SchResource.AETHERFLOW] -= 1
                if resources[SchResource.AETHERFLOW] < 0:
                    notices.add(SchSimNotice.SCH_SIM_AETHERFLOW_OVERSPENDING)
            elif selected_action == SchAction.SWIFTCAST:
                active_effects[SchEffect.SWIFTCAST] = current_time + 10
            elif selected_action == SchAction.BIOLYSIS:
                active_effects[SchEffect.BIOLYSIS] = current_time + 30

            # advance time based on cast time or animation lock as needed
            current_time += \
                max(cast_time + caster_tax, animation_lock)

        return SchSimResults(timeline, notices)

    def get_pps(self, character_stats, caster_tax=0.1, num_ed_per_min=4, num_filler_casts=0):
        """
        Get the expected PPS.
        A port of the sch spreadsheet's pps function.
        """
        return self.total_potency_spreadsheet_port(
            character_stats, caster_tax, num_ed_per_min, num_filler_casts) / self.get_cycle(
                character_stats, caster_tax)

    def get_mp_per_min(self, character_stats, caster_tax=0.1, succ=0, adlo=0, energy_drain=4, rez=0): # pylint: disable=too-many-arguments
        """
        Get the expected mp consumption in a minute.
        """
        cycle = self.get_cycle(character_stats, caster_tax)
        mpps = self.mp_consumed_per_cycle(
            character_stats, caster_tax, succ, adlo, energy_drain, rez, cycle) / cycle
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
    def mp_consumed_per_cycle(cls, character_stats, caster_tax, succ, adlo, energy_drain, rez, cycle): # pylint: disable=too-many-arguments
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
        result -= 500 * energy_drain * cycle / 60
        return result

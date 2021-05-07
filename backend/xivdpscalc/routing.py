"""Routing logic for ffxiv-dps-calc backend"""

from flask import jsonify, request, abort
import requests

from xivdpscalc import app # pylint: disable=cyclic-import
from xivdpscalc.character import Character, CharacterStatSpread
from xivdpscalc.character.jobs import Comp, Jobs
from xivdpscalc.pps.sch import SchPps

@app.route('/update_stats', methods=["POST"])
def update_stats():
    """Calculates damage, mp consumption, and gcd based on input.
    Accepts and returns JSON. JSON format is as follows:
    input: {'player': Object
                {'weaponDamage': int
                'mainStat': int
                'det': int
                'crit': int
                'dh': int
                'speed': int
                'ten': int
                'pie': int}
            'job': string
            'comp': Array
            'rotation': Object
                {'adloquium': int
                 'energyDrain': int
                 'raise': int
                 'succor': int}}
    output: {'dps': float,
             'gcd': float,
             'mp': float}
    """
    data = request.get_json()

    if not data:
        return "abort", abort(400)

    player_data = data['player']

    try:
        my_job = Jobs.create_job(data['job'])[0]
    except KeyError:
        return f"Currently {data['job']} is not supported."

    player = Character(
        my_job,
        CharacterStatSpread(
            wd = player_data['weaponDamage'],
            mainstat = player_data['mainStat'],
            det = player_data['det'],
            crit = player_data['crit'],
            dh = player_data['dh'],
            speed = player_data['speed'],
            ten = player_data['ten'],
            pie = player_data['pie']
        )
    )

    try:
        rotation_data = data['rotation']
        energy_drain_per_min = rotation_data.get('energyDrain', 4)
        adloquium_per_min = rotation_data.get('adloquium', 0)
        raise_per_min = rotation_data.get('raise', 0)
        succor_per_min = rotation_data.get('succor', 0)
    except KeyError:
        # Rotation data was not present in request, use defaults
        energy_drain_per_min, adloquium_per_min, raise_per_min, succor_per_min = 4, 0, 0, 0
    filler_casts_per_min = adloquium_per_min + raise_per_min + succor_per_min

    my_sch_pps = SchPps()
    potency = my_sch_pps.get_pps(player, num_ed_per_min=energy_drain_per_min, num_filler_casts=filler_casts_per_min)
    try:
        comp_jobs = [Jobs.create_job(comp_job)[0] for comp_job in data['comp']]
    except KeyError:
        return "A job was not supported in that team comp."

    my_comp = Comp(comp_jobs)

    dps = round(player.calc_damage(potency, my_comp), 2)
    gcd = player.get_gcd()
    mp = round(my_sch_pps.get_mp_per_min(player,
                                         succ=succor_per_min,
                                         adlo=adloquium_per_min,
                                         energy_drain=energy_drain_per_min,
                                         rez=raise_per_min), 2)
    return jsonify({"dps": dps,
                    "gcd": gcd,
                    "mp": mp})


# TODO: pull out repeated code and update it to match update_stats()
@app.route('/calc_damage/etro', methods=["POST"])
def etro_main():
    """Calculates damage, given a gearsetID from Etro. Should check database to see if gearset exist first.
    JSON format:
    'job': String,
    'comp': Array,
    'etro_id': String,
    """

    data = request.get_json()

    # Check comp first before making request
    if not data:
        return "abort", abort(400)
    try:
        comp_jobs = [Jobs.create_job(comp_job)[0] for comp_job in data['comp']]
    except KeyError:
        return "An unsupported job was found in the team composition."

    my_comp = Comp(comp_jobs)

    player_job_data = Jobs.create_job(data['job'])

    # TODO: Check internal database to see if cached before request

    try:
        etro_data = requests.get("/".join(["https://etro.gg/api/gearsets", data["etro_id"]])).json()
    except requests.exceptions.RequestException:
        return "There was an error making the etro request"

    etro_stats = etro_data["totalParams"]
    eq_stats = {stat["name"]: stat["value"] for stat in etro_stats}

    # For Etro sets that are non-tanks
    if "TEN" not in eq_stats:
        eq_stats["TEN"] = 0

    # Making speed job-agnostic
    if "SPS" in eq_stats:
        eq_stats["SPEED"] = eq_stats["SPS"]
    else:
        eq_stats["SPEED"] = eq_stats["SKS"]

    player = Character(
        player_job_data[0],
        CharacterStatSpread(
            wd = eq_stats["Weapon Damage"],
            mainstat = eq_stats[player_job_data[1]],
            det = eq_stats["DET"],
            crit = eq_stats["CRT"],
            dh = eq_stats["DH"],
            speed = eq_stats["SPEED"],
            ten = eq_stats["TEN"],
            pie = eq_stats["PIE"]
        )
    )

    my_sch_pps = SchPps()
    potency = my_sch_pps.get_pps(player)

    dps = round(player.calc_damage(potency, my_comp), 2)
    gcd = player.get_gcd()
    mp = round(my_sch_pps.get_mp_per_min(player), 2)
    return jsonify({"dps": dps,
                    "gcd": gcd,
                    "mp": mp})

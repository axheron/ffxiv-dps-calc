from flask import Flask, jsonify, request, abort

from backend.calc import CharacterStats, Comp, Jobs
from backend.pps.sch import SchPps

app = Flask(__name__)


@app.route('/calc_damage', methods=["POST"])
def main():
    """Calculates damage based on input. Accepts and returns JSON. JSON format is as follows:
    'player': Object
        'job': string
        'wd': int
        'mainstat': int
        'det': int
        'crit': int
        'dh': int
        'speed': int
        'ten': int
        'pie': int
    'comp': Array
    """
    data = request.get_json()

    if not data:
        return "abort", abort(400)

    # Convert job strings to enum
    job_string_to_enum = {
        "SCH": Jobs.SCH,
        "AST": Jobs.AST,
        "WHM": Jobs.WHM,
        "PLD": Jobs.PLD,
        "WAR": Jobs.WAR,
        "DRK": Jobs.DRK,
        "GNB": Jobs.GNB,
        "NIN": Jobs.NIN,
        "DRG": Jobs.DRG,
        "MNK": Jobs.MNK,
        "SAM": Jobs.SAM,
        "MCH": Jobs.MCH,
        "DNC": Jobs.DNC,
        "BRD": Jobs.BRD,
        "SMN": Jobs.SMN,
        "BLM": Jobs.BLM,
        "RDM": Jobs.RDM,
    }
    
    player_data = data['player']

    my_job = job_string_to_enum[player_data["job"]]
    player = CharacterStats(
        my_job,
        player_data['wd'],
        player_data['mainstat'],
        player_data['det'],
        player_data['crit'],
        player_data['dh'],
        player_data['speed'],
        player_data['ten'],
        player_data['pie']
    )
    my_sch_pps = SchPps()
    potency = my_sch_pps.get_pps(player)
    comp_jobs = [job_string_to_enum[comp_job] for comp_job in data['comp']]
    my_comp = Comp(comp_jobs)

    dps = player.calc_damage(potency, my_comp)
    return jsonify({"dps": dps})


if __name__ == "__main__":
    app.run()

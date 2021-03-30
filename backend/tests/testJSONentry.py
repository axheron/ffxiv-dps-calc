from backend.main import app
from flask import json


def test_json_calc():
    response = app.test_client().post(
        '/calc_damage',
        data=json.dumps({
            'player': {
                'job': 'SCH',
                'wd': 180,
                'mainstat': 5577,
                'det': 2272,
                'crit': 3802,
                'dh': 1100,
                'speed': 2139,
                'ten': 380,
                'pie': 340,
            },
            'comp': ['PLD', 'WAR', 'SCH', 'AST', 'SAM', 'NIN', 'MCH', 'SMN']
        }),
        content_type='application/json',
    )

    res = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert res['dps'] == 14238.04118

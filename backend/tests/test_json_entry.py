''' Tests for the json parsing and etro import '''

from xivdpscalc.main import app
from flask import json


def test_json_calc():
    response = app.test_client().post(
        '/calc_damage',
        data=json.dumps({
            'player': {
                'wd': 180,
                'mainstat': 5577,
                'det': 2272,
                'crit': 3802,
                'dh': 1100,
                'speed': 2139,
                'ten': 380,
                'pie': 340,
            },
            'comp': ['PLD', 'WAR', 'SCH', 'AST', 'SAM', 'NIN', 'MCH', 'SMN'],
            'job': 'SCH',
        }),
        content_type='application/json',
    )

    res = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert res['dps'] == 14238.04118


def test_etro_calc():
    response = app.test_client().post(
        '/calc_damage/etro',
        data=json.dumps({
            'job': 'SCH',
            'comp': ['PLD', 'WAR', 'SCH', 'AST', 'SAM', 'NIN', 'MCH', 'SMN'],
            'etro_id': '1652ae0d-deea-4d86-9b4e-f5959f5232d4',
        }),
        content_type='application/json',
    )

    res = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    # TODO: add assert that tests return value
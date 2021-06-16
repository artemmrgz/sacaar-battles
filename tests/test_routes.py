import pytest
import os
import json
from sacaar_battles.app import db, app
from sacaar_battles.tests.fixtures.data import heroes


FIXTURES = os.path.join('tests', 'fixtures')


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    db.create_all()
    for hero in heroes:
        db.session.add(hero)
    db.session.commit()
    client = app.test_client()
    return client


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.get_data() == b'Welcome to the Sacaar Battles!'


def test_rating(client):
    res = client.get('/characters')
    with open(os.path.join(FIXTURES, 'characters.json')) as f:
        expected = json.load(f)
    assert res.status_code == 200
    assert res.get_json() == expected


def test_kill(client):
    res = client.post('/kill/1')
    assert res.status_code == 200
    assert res.get_json()['killed']['name'] == 'frigga'


def test_killed(client):
    res = client.get('/killed')
    assert res.status_code == 200
    assert len(res.get_json()['killed']) == 3


def test_battle(client):
    res = client.get('/battle')
    assert res.status_code == 200
    assert len(res.get_json()['battle']) == 2
    assert res.get_json()['battle']['first fighter']['race'] == res.get_json()['battle']['second fighter']['race']

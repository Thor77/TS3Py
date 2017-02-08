import pytest

from ts3py.testing import build_command


@pytest.fixture
def client(virtual_server):
    with virtual_server.query.respond({
        'clientlist': [{
            'clid': 1,
            'cid': 9,
            'client_database_id': 591,
            'client_nickname': 'Someone',
            'client_type': 0
        }]
    }):
        return virtual_server.clients[0]


def test_repr(client):
    assert repr(client) == client.client_nickname


def test_poke(client):
    with client.server.query.assert_sent([build_command('clientpoke', params={
        'clid': client.clid,
        'msg': 'Test'
    })]):
        client.poke('Test')


def test_ban(client):
    with client.server.query.assert_sent([build_command('banclient', params={
        'clid': client.clid,
        'time': 60,
        'banreason': 'Test'
    })]):
        client.ban(duration=60, reason='Test')

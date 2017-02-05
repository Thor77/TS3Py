import pytest


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

import pytest


@pytest.fixture
def channel(virtual_server):
    with virtual_server.query.respond({
        'channellist': [{
            'cid': 1,
            'pid': 0,
            'channel_order': 0,
            'channel_name': 'Great channel',
            'total_clients': 0,
            'channel_needed_subscribe_power': 0
        }]
    }):
        return virtual_server.channel[0]


def test_repr(channel):
    assert repr(channel) == channel.channel_name


def test_clients(channel):
    with channel.server.query.respond({
        'clientlist': [
            {
                'cid': 1,
                'clid': 1,
                'client_nickname': 'Someone'
            },
            {
                'cid': 5,
                'clid': 2,
                'client_nickname': 'Someone else'
            }
        ]
    }):
        clients = channel.clients
        assert len(clients) == 1
        assert clients[0].clid == 1

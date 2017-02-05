from ts3py.testing import build_command


def test_repr(virtual_server):
    assert repr(virtual_server) == virtual_server.virtualserver_name


def test_command(virtual_server):
    assert virtual_server.virtualserver_id == 1
    # test use command here inititially => no need to assert it for every test
    with virtual_server.query.assert_sent([
        build_command('use', params={'sid': virtual_server.virtualserver_id}),
        build_command('help')
    ]):
        virtual_server.command('help')


def test_clients(virtual_server):
    with virtual_server.query.respond({
        'clientlist': [{
            'client_nickname': 'Someone'
        }]
    }):
        clients = virtual_server.clients
        assert len(clients) == 1
        assert clients[0].virtualserver_id == virtual_server.virtualserver_id


def test_channel(virtual_server):
    with virtual_server.query.respond({
        'channellist': [{
            'channel_name': 'Great channel'
        }]
    }):
        channel = virtual_server.channel
        assert len(channel) == 1
        assert channel[0].virtualserver_id == virtual_server.virtualserver_id

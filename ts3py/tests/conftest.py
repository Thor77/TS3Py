import pytest

from ts3py.testing import TestingServer


@pytest.fixture
def server():
    return TestingServer()


@pytest.fixture
def virtual_server(server):
    with server.query.respond({
        'serverlist': [{
            'virtualserver_id': 1,
            'virtualserver_port': 9987,
            'virtualserver_status': 'online',
            'virtualserver_clientsonline': 50,
            'virtualserver_queryclientsonline': 50,
            'virtualserver_maxclients': 100,
            'virtualserver_uptime': 60,
            'virtualserver_name': 'Server for testing stuff',
            'virtualserver_autostart': 1
        }]
    }):
        return server.virtual_servers[0]

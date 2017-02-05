from ts3py.testing import build_command


def test_virtual_servers(server):
    with server.query.respond({
        'serverlist': [{
            'virtualserver_name': 'Server for testing stuff'
        }]
    }):
        assert len(server.virtual_servers) == 1


def test_login(server):
    with server.query.assert_sent([build_command('login', params={
        'client_login_name': 'serveradmin',
        'client_login_password': '123456'
    })]):
        server.login('serveradmin', '123456')


def test_logout(server):
    with server.query.assert_sent([build_command('logout')]):
        server.logout()


def test_gm(server):
    with server.query.assert_sent([
        build_command('gm', params={'msg': 'Important message'})
    ]):
        server.gm('Important message')

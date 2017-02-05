from .virtual_server import VirtualServer
from ts3py.query import Query


class Server:
    def __init__(self, host, port=10011):
        self.query = Query(host, port)

    @property
    def virtual_servers(self):
        '''
        Return a list of virtual-servers on that server.

        :return: list of virtual-servers
        :rtype: list
        '''
        def _virtual_servers():
            serverlist = self.query.command('serverlist')
            for server_data in serverlist:
                virtual_server = VirtualServer(self.query, server_data)
                yield virtual_server
        return list(_virtual_servers())

    def __repr__(self):
        return str(self.virtualserver_name)

    def login(self, username, password):
        '''
        Login to an user-account on the server.

        :param username: name of the user
        :param password: password of the user
        '''
        self.query.command('login', params={
            'client_login_name': username, 'client_login_password': password
        })

    def logout(self):
        '''
        Logout from the current session
        '''
        self.query.command('logout')

    def gm(self, message):
        '''
        Send a text message to all clients on all virtual servers

        :param message: message to be sent

        :type message: str
        '''
        self.query.command('gm', params={
            'msg': message
        })

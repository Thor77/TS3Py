from ts3py.objects import VirtualServer
from ts3py.query import Query


class Server:
    def __init__(self, ip, port=10011):
        self.query = Query(ip, port)

    @property
    def virtual_servers(self):
        def _virtual_servers():
            serverlist = self.query.command('serverlist')
            for server_data in serverlist:
                virtual_server = VirtualServer(self.query)
                for key, value in server_data.items():
                    setattr(virtual_server, key, value)
                yield virtual_server
        return list(_virtual_servers())

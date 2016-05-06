from ts3py.objects import Client


class Channel:
    def __init__(self, server):
        self.server = server

    @property
    def clients(self):
        def _clients():
            clientlist = self.server.command('clientlist')
            clientlist = filter(lambda c: c['cid'] == self.cid, clientlist)
            for client_data in clientlist:
                client = Client(self.server)
                for key, value in client_data.items():
                    setattr(client, key, value)
                yield client
        return list(_clients())

    def __repr__(self):
        return str(self.channel_name)

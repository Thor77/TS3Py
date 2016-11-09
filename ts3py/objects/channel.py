from .client import Client
from .proto import Proto


class Channel(Proto):
    @property
    def clients(self):
        '''
        Return a list of clients in that channel.

        :return: list of clients
        :rtype: list
        '''
        def _clients():
            clientlist = self.server.command('clientlist')
            clientlist = filter(lambda c: c['cid'] == self.cid, clientlist)
            for client_data in clientlist:
                client = Client(self.server, client_data)
                yield client
        return list(_clients())

    def __repr__(self):
        return str(self.channel_name)

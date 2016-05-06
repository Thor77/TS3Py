from ts3py.objects import Channel, Client


class VirtualServer:
    def __init__(self, query):
        self.query = query

    def command(self, cmd, params={}, options=[]):
        '''
        Run a command in the context of the virtual-server.

        :param cmd: command
        :param params: parameters appended to the command
        :param options: options appended to the command
        :type cmd: string
        :type params: dict
        :type options: list

        :return: response of the command (if any)
        :rtype: list
        '''
        self.query.command('use', params={'sid': self.virtualserver_id})
        return self.query.command(cmd, params, options)

    @property
    def clients(self):
        '''
        Return a list of clients on that virtual-server.

        :return: list of clients
        :rtype: list
        '''
        def _clients():
            clientlist = self.command('clientlist')
            for client_data in clientlist:
                client = Client(self)
                client.virtualserver_id = self.virtualserver_id
                for key, value in client_data.items():
                    setattr(client, key, value)
                yield client
        return list(_clients())

    @property
    def channel(self):
        '''
        Return a list of channel on that virtual-server.

        :return: list of channel
        :rtype: list
        '''
        def _channel():
            channellist = self.command('channellist')
            for channel_data in channellist:
                channel = Channel(self)
                channel.virtualserver_id = self.virtualserver_id
                for key, value in channel_data.items():
                    setattr(channel, key, value)
                yield channel
        return list(_channel())

    def __repr__(self):
        return str(self.virtualserver_name)

from .proto import Proto


class Client(Proto):
    def __repr__(self):
        return str(self.client_nickname)

    def poke(self, message):
        self.server.command('clientpoke', params={
            'clid': self.clid,
            'msg': message
        })

    def ban(self, duration=None, reason=None):
        params = {'clid': self.clid}
        if duration:
            params['time'] = duration
        if reason:
            params['banreason'] = reason
        self.server.command('banclient', params=params)

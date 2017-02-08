from .proto import Proto


class Client(Proto):
    def __repr__(self):
        return str(self.client_nickname)

    def poke(self, message):
        self.server.command('clientpoke', params={
            'clid': self.clid,
            'msg': message
        })

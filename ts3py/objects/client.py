from ts3py.objects.proto import TS3ObjectProto


class Client(TS3ObjectProto):
    def __repr__(self):
        return str(self.client_nickname)

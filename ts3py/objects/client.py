from ts3py.objects.proto import Proto


class Client(Proto):
    def __repr__(self):
        return str(self.client_nickname)

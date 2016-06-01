class TS3ObjectProto:
    def __init__(self, server, params={}):
        self.server = server
        for key, value in params.items():
            setattr(self, key, value)

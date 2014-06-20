import inspect

class Plugin:

    def __init__(self, bot):
        self.bot = bot
        if hasattr(self, 'onLoad') and inspect.ismethod(getattr(self, 'onLoad')):
            self.onLoad()

    def registerCommand(self, cmd, func, helpstring):
        '''
        Register command
        '''
        self.bot.registerCommand(cmd, func, helpstring)

    def unregisterCommand(self, cmd):
        '''
        Unregister command
        '''
        self.bot.unregisterCommand(cmd)

    def registerEvent(self, event, func):
        '''
        if found_event == event: func(data, event_data)
        '''
        self.bot.registerEvent(event, func)

    def command(self, cmd, params={}, options=[]):
        '''
        Send query-cmd to the server
        '''
        return self.bot.command(cmd, params, options)

    def sendtextmessageClient(self, target_id, msg):
        '''
        Send textmessage to client
        '''
        self.bot.sendtextmessageClient(target_id, msg)

    def sendtextmessageChannel(self, target_id, msg):
        '''
        Send textmessage to channel
        '''
        self.bot.sendtextmessageChannel(target_id, msg)

    def sendtextmessageServer(self, target_id, msg):
        '''
        Send textmessage to server
        '''
        self.bot.sendtextmessageServer(target_id, msg)

    def clientpoke(self, target_id, msg):
        '''
        Poke client
        '''
        self.bot.clientpoke(target_id, msg)

    def unload(self):
        if hasattr(self, 'onUnload') and inspect.ismethod(getattr, 'onUnload'):
            self.onUnload()

    def getName(self):
        return self.__class__.__name__
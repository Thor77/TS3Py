import inspect

class Plugin:
    
    def __init__(self, bot):
        self.bot = bot
        if hasattr(self, 'onLoad') and inspect.ismethod(getattr(self, 'onLoad')):
            self.onLoad()

    def addCommand(self, trg, func, helpstring):
        self.bot.addCommand(trg, func, helpstring)

    def sendTextmessageClient(self, target_id, msg):
        self.bot.sendTextmessageClient(target_id, msg)

    def sendTextmessageChannel(self, target_id, msg):
        self.bot.sendTextmessageChannel(target_id, msg)

    def sendTextmessageServer(self, target_id, msg):
        self.bot.sendTextmessageServer(target_id, msg)

    def poke(self, target_id, msg):
        self.bot.poke(target_id, msg)

    def unload(self):
        if hasattr(self, 'onUnload') and inspect.ismethod(getattr(self, 'onUnload')):
            self.onUnload()

    def getName(self):
        return self.__class__.__name__
import inspect

class Plugin:
    
    def __init__(self, bot):
        self.bot = bot
        if hasattr(self, 'onLoad') and inspect.ismethod(getattr(self, 'onLoad')):
            self.onLoad()

    def addCommand(self, trg, func, helpstring):
        self.bot.addCommand(trg, func, helpstring)

    def sendtextmessageClient(self, target_id, msg):
        self.bot.sendtextmessageClient(target_id, msg)

    def sendtextmessageChannel(self, target_id, msg):
        self.bot.sendtextmessageChannel(target_id, msg)

    def sendtextmessageServer(self, target_id, msg):
        self.bot.sendtextmessageServer(target_id, msg)

    def clientpoke(self, target_id, msg):
        self.bot.clientpoke(target_id, msg)

    def registerNotify(self, notify_name, func):
        self.bot.registerNotify(notify_name, func)

    def command(self, cmd, parameter={}, options=[]):
        return self.bot.command(cmd, parameter, options)

    def unload(self):
        if hasattr(self, 'onUnload') and inspect.ismethod(getattr(self, 'onUnload')):
            self.onUnload()

    def getName(self):
        return self.__class__.__name__
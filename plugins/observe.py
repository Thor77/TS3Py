from plugin import Plugin
from ts3bot import FuncThread

class Observer(Plugin):

    def onLoad(self):
        self.funcThread = FuncThread(self.observe, 60)
        self.funcThread.start() # start observer-thread
        self.blocklist = ['insert', 'strings', 'here'] # blocklist
        # commands

    def observe(self):
        print('observing...')
        chanlist = self.bot.channellist()
        for channel in chanlist:
            cname = chanlist[channel]['channel_name'].lower()
            if 'channel_topic' in chanlist[channel]:
                ctopic = chanlist[channel]['channel_topic'].lower()
            else:
                ctopic = ''
            if any(string.lower() in cname or string.lower() in ctopic for string in self.blocklist):
                self.bot.channeldelete(channel)
                print('channel %s deleted because "%s"!' % (cname, string))

    def onUnload(self):
        self.funcThread.stop()
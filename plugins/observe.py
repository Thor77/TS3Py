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
        print(chanlist)
        for channel in chanlist:
            cname = chanlist[channel]['channel_name'].lower()
            if 'channel_topic' in chanlist[channel]:
                ctopic = chanlist[channel]['channel_topic'].lower()
            else:
                ctopic = ''
            for string in self.blocklist:
                string = string.lower()
                if cname.find(string) != -1 or ctopic.find(string) != -1:
                    self.bot.channeldelete(channel)
                    print('Channel %s deleted because "%s"!' % (cname, string))

    def onUnload(self):
        self.funcThread.stop()
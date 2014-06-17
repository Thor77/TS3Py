from plugin import Plugin
from threading import Thread
from threading import Event

class Channelobserve(Plugin):

    def onLoad(self):
        self.stopFlag = Event()
        self.observer_thread = Observer(self.stopFlag, self.observe, 20)
        self.blocklist = ['führer', 'konzentration', 'lager', '']
        # commands

    def observe(self):
        channellist = self.getChannellist()
        for cid in channellist:
            channelname = channellist[cid].lower()
            for string in self.blocklist:
                if channelname.find(string.lower()) != 0:
                    self.bot.deleteChannel(cid)

    def onUnload(self):
        self.stopFlag.set()

class Observer(Thread):
    def __init__(self, event, function, delay):
        Thread.__init__(self)
        self.stopped = event
        self.function = function
        self.delay = delay

    def run(self):
        while not self.stopped.wait(self.delay):
            self.function()
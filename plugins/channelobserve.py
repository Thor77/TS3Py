from plugin import Plugin
from threading import Thread
from threading import Event

class Channelobserve(Plugin):

    def onLoad(self):
        self.stopFlag = Event()
        self.observer_thread = Observer(self.stopFlag, self.observe, 20)
        #self.observer_thread.start()
        self.blocklist = ['führer', 'konzentration', 'lager']
        # commands

    def observe(self):
        print('observing')
        channellist = self.bot.channellist()
        for cid in channellist:
            channelname = channellist[cid]['channel_name'].lower()
            channeltopic = channellist[cid]['channel_topic'].lower()
            for string in self.blocklist:
                print('String: %s Name: %s' % (string, channelname))
                if channelname.find(string.lower()) != -1 or channeltopic.find(string.lower()) != -1:
                    self.bot.channeldelete(cid)

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
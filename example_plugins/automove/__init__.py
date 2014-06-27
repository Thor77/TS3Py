from plugin import Plugin
from ts3bot import FuncThread
import configparser

class Automove(Plugin):

    def onLoad(self):
        self.clients = {} # {clid: [oldchanid, times_observed, moved]}
        self.readConfig()
        self.observeThread = FuncThread(self.observe, 10)
        self.observeThread.start()

    def observe(self):
        print('looking...')
        clientlist = self.clientlist()
        for clid in clientlist:
            clinfo = clientlist[clid]
            afk_channel = self.afk_channel_id
            curr_channel = clinfo['cid']
            if bool(int(clinfo['client_input_muted'])) or bool(int(clinfo['client_output_muted'])) or not bool(int(clinfo['client_input_hardware'])) or not bool(int(clinfo['client_output_hardware'])) or bool(int(clinfo['client_away'])):
                # client is afk
                if clid in self.clients:
                    cl = self.clients[clid]
                    if not cl[2] and cl[1] >= (self.minutes_until_move * 2) and not curr_channel == afk_channel: # *2 because looking every 30sek
                        self.clients[clid][0] = curr_channel
                        self.clients[clid][2] = True
                        self.clients[clid][1] = 0
                        self.bot.clientmove(clid, afk_channel)
                        print('%s is afk!' % clinfo['client_nickname'])
                    else:
                        self.clients[clid][1] += 1
                else:
                    self.clients[clid] = [1, 1, False]
            else:
                if clid in self.clients:
                    cl = self.clients[clid]
                    if cl[2]:
                        print('%s is back!' % clinfo['client_nickname'])
                        if str(curr_channel) == str(afk_channel):
                            # move back
                            self.bot.clientmove(clid, cl[0])
                        self.clients[clid][2] = False
                        self.clients[clid][1] = 0

    def readConfig(self):
        filename = 'plugins/automove/cfg.ini'
        config = configparser.ConfigParser()
        config.read(filename)
        self.minutes_until_move = int(config['Automove']['move_delay'])
        self.afk_channel_id = config['Automove']['afk_channel_id']

    def clientlist(self):
        raw = self.command('clientlist', options=['info', 'country', 'away', 'voice'])
        info = {}
        for client in raw:
            if client['client_type'] == 0:
                clid = client['clid']
                del client['clid']
                info[clid] = client
        return info

    def onUnload(self):
        self.observeThread.stop()
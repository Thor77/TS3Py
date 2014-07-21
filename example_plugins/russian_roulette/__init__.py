from plugin import Plugin
import random

class RussianRoulette(Plugin):

    def onLoad(self):
        self.chance = 1, 5
        self.chance_list = []
        # commands
        self.registerCommand('rr', self.rr_func, 'Russian Roulette')

    def choice(self):
        if len(self.chance_list) <= 0:
            trues, falses = self.chance
            self.chance_list = (trues * [True]) + (falses * [False])
            random.shuffle(self.chance_list)
        return self.chance_list.pop(0)

    def rr_func(self, params, clid, clname):
        cid = self.bot.clientinfo(clid)['cid']
        clientlist = self.bot.clientlist()
        clients = []
        for client in clientlist:
            if clientlist[client]['cid'] == cid:
                clients.append(client)
        if len(clients) <= 1:
            self.sendtextmessageClient(clid, 'You can\'t play russian roulette alone!')
        elif not self.choice():
            self.sendtextmessageClient(clid, 'Nothing happened...')
        else:
            client = random.choice(clients)
            self.clientpoke(client, 'You was shot!')
            self.bot.clientkickServer(client, 'Booooooom')
from plugin import Plugin
import random

class RussianRoulette(Plugin):

    def onLoad(self):
        self.chance = 1, 5
        # commands
        self.registerCommand('rr', self.rr_func, 'Russian Roulette')

    def rr_func(self, params, clid, clname):
        trues, falses = self.chance
        chance = (trues * [True]) + (falses * [False])
        if not random.choice(chance):
            self.sendtextmessageClient(clid, 'Nothing happended...')
        cid = self.bot.clientinfo(clid)['cid']
        clientlist = self.bot.clientlist()
        clients = []
        for client in clientlist:
            if clientlist[client]['cid'] == cid:
                clients.append(client)
        if len(clients) <= 1:
            self.sendtextmessageClient(clid, 'You can\'t play russian roulette alone!')
            return
        client = random.choice(clients)
        self.clientpoke(client, 'You was shot!')
        self.bot.clientkickServer(client, 'Booooooom')
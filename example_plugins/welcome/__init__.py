from plugin import Plugin
from ts3py import TS3Error
import time

class Welcome(Plugin):

    def onLoad(self):
        # commands and events
        self.registerEvent('notifycliententerview', self.onClientJoin)

    def onClientJoin(self, data):
        try:
            if data['client_type'] != 0:
                print('Query-Client joined!')
                return
        except KeyError:
            print(TS3Error('Got invalid data!'))
            return

        dbid = data['client_database_id']
        nick = data['client_nickname']
        info = self.command('clientdbinfo', {'cldbid': dbid})
        t = time.gmtime(int(info['client_created']))
        seconds = str(t[5])
        if len(seconds) == 1:
            seconds = '0%s' % seconds
        first_visit = '{day}.{month}.{year} um {hours}:{minutes}:{seconds}'.format(day=t[2], month=t[1], year=t[0], hours=t[3], minutes=t[4], seconds=seconds)
        self.sendtextmessageClient(data['clid'], 'Hallo %s, dies ist dein %s. Besuch, der erste war am %s!' % (nick, info['client_totalconnections'], first_visit))
        print('%s joined!' % nick)
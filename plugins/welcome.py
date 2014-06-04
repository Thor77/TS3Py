from plugin import Plugin
import time

class Welcome(Plugin):

    def onLoad(self):
        self.registerNotify('notifycliententerview', self.onJoin)

    def onJoin(self, name, data):
        try:
            if data['client_unique_identifier'] == 'ServerQuery' or data['client_type'] != '0':
                print('Query-Client joined!')
                return
        except:
            print('Error finding client-type!')
            return
        database_id = data['client_database_id']
        nick = data['client_nickname']
        info = self.sendCommand('clientdbinfo', {'cldbid': database_id})
        t = time.gmtime(int(info['client_created']))
        seconds = str(t[5])
        if len(seconds) == 1:
            seconds = '0%s' % seconds
        first_visit = '{day}.{month}.{year} um {hours}:{minutes}:{seconds}'.format(day=t[2], month=t[1], year=t[0], hours=t[3], minutes=t[4], seconds=seconds)
        self.sendTextmessageClient(data['clid'], 'Hallo %s, dies ist dein %s. Besuch, der erste war am %s!' % (nick, info['client_totalconnections'], first_visit))
        print('%s joined!' % nick)
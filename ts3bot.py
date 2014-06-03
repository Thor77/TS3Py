from pyts3 import ServerQuery
import time

'''
server = ServerQuery('95.143.172.216', 61962)
server.connect()
server.login('serveradmin', 'zNSWXdXh')
server.use(1)
server.command('clientupdate', {'client_nickname': 'Thor77s PyTS3-Bot'})
#print('VirtualServers: %s' % server.getServerlist())
#print('Channels: %s' % server.getChannellist())
#print('Clients: %s' % server.getClientlist())

call = '!'
# register events and notifys
def onUserJoin(name, data):
    # check if user is ServerQuery
    if data['client_type'] == '0':
        print('Client %s from %s joined the server!' % (data['client_nickname'], data['client_country']))
        server.sendTextmessageClient(data['clid'], 'Hallo %s, herzlich willkommen auf Thor77s TeamspeakServer!')
        if data['client_country'] != 'DE':
            server.sendTextmessageClient(data['clid'], 'Wie ich sehe verbindest du dich nicht aus Deutschland. Auf diesem Server wird ausschließlich Deutsch gesprochen!')

def onCommand(cmd, client_id, client_name):
    print('Got command from %s (%s): %s' % (client_name, client_id, cmd))
    if cmd == 'commands':
        server.sendTextmessageClient(client_id, 'List of commands: \n!commands list of commands')

def onTextMessage(name, data):
    if data['client_type'] == '0':
        msg = data['msg']
        if msg[:len(call)] == call:
            onCommand(msg[len(call):], data['invokerid'], data['invokername'])
        server.sendTextmessageClient(data['invokerid'], 'Hallo %s!' % data['invokername'])

# register all events
server.registerEvent('textserver')
server.registerEvent('textchannel')
server.registerEvent('textprivate')
server.registerEvent('server')
# register notifys
server.registerNotify('notifycliententerview', onUserJoin)
server.registerNotify('notifytextmessage', onTextMessage)
#server.notifyAll(everything)

# wait for events
print('Waiting for events...')
while True:
    time.sleep(0.5)
'''

class TS3Py(ServerQuery):
    def __init__(self, ip, port, call='!'):
        ServerQuery.__init__(self, ip, port)
        self.commands = {}
        self.call = call

    def gotCommand(self, command, params, client_id, client_name):
        if command in self.commands:
            self.commands[command]['func'](params, client_id, client_name)

    def addCommand(self, cmd, func, helpstring):
        if cmd not in self.commands:
            self.commands[cmd] = {'func': func, 'help': helpstring}

    def deleteCommand(self, cmd):
        if cmd in self.commands:
            del self.commands[cmd]

    def deleteAllCommands(self):
        self.commands = {}

    def _onTextmessage(self, name, data):
        print(name)
        print(data)
        #if data['client_type'] == '0':
        msg = data['msg']
        msg = msg.strip()
        if msg[:len(self.call)]:
            params = msg.split(' ')[1:]
            self.gotCommand(msg[len(self.call):], params, data['invokerid'], data['invokername'])

    def start(self):
        self.registerEvent('textserver')
        self.registerEvent('textchannel')
        self.registerEvent('textprivate')
        self.registerEvent('server')

        self.registerNotify('notifytextmessage', self._onTextmessage)
        # default commands
        # help command
        self.addCommand('help', self.help, 'Show help message and list commands')

        # start mainloop
        print('Waiting for events...')
        while True:
            time.sleep(0.5)

    def help(self, params, client_id, client_name):
        if len(params) == 0:
            helpstring = []
            helpstring.append('--list of commands--')
            helpstring.append('Syntax: \'command\' -> \'helpstring\'')
            for cmd in self.commands:
                cmddict = self.commands[cmd]
                helpstring.append('%s -> %s' % (cmd, cmddict['help']))
            helpstring.append('\n\nUse %shelp \'command\' to get help about a specific command!' % self.call)
            self.sendTextmessageClient(client_id, '\n'.join(helpstring))
        else:
            command = params[0]
            if command in self.commands:
                self.sendTextmessageClient(client_id, 'Help about %s:\n%s' % (command, self.commands[command]['help']))
            else:
                self.sendTextmessageClient(client_id, 'Invalid command! Try \'%shelp\' for a list of commands!' % self.call)

bot = TS3Py('95.143.172.216', 61962)
bot.connect()
bot.login('serveradmin', 'zNSWXdXh')
bot.use(1)
bot.start()
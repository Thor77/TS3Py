from ts3py import TS3Query
import _thread
import imp
import pkgutil
import inspect
import plugins
from plugin import Plugin

class TS3Bot(TS3Query):
    def __init__(self, ip, port, call='!'):
        TS3Query.__init__(self, ip, port)
        # server notifications things
        self.LastCommand = 0
        self.Lock = _thread.allocate_lock()
        self.RegisteredNotifys = []
        self.RegisteredEvents = []
        _thread.start_new_thread(self.worker, ())
        self.notifyAllactivated = False
        self.notifyAll_func = None
        # command and plugin variables
        self.commands = {}
        self.call = call
        self.plugins = []

    # command functions
    def gotCommand(self, command, params, client_id, client_name):
        '''
        Handle command
        '''
        if command in self.commands:
            self.commands[command]['func'](params, client_id, client_name)

    def addCommand(self, cmd, func, helpstring):
        '''
        Register a command
        '''
        if cmd not in self.commands:
            self.commands[cmd] = {'func': func, 'help': helpstring}

    def deleteCommand(self, cmd):
        '''
        Delete a command
        '''
        if cmd in self.commands:
            del self.commands[cmd]

    def deleteAllCommands(self):
        '''
        Delete all commands
        '''
        self.commands = {}

    def messageFindCommand(self, name, data):
        '''
        Find command in message
        '''
        #print(name)
        #print(data)
        #if data['client_type'] == '0':
        msg = data['msg']
        msg = msg.strip()
        if msg[:len(self.call)]:
            command = msg[len(self.call):].split(' ')[0]
            params = msg.split(' ')[1:]
            self.gotCommand(command, params, data['invokerid'], data['invokername'])

    # plugin functions
    def unloadPlugins(self):
        '''
        Unload all plugins
        '''
        self.deleteAllCommands()
        self.unregisterAllNotifys()
        for plugin in self.plugins:
            plugin.unload()
        self.plugins = []

    def loadPlugin(self, modname):
        '''
        Load plugin
        '''
        module = __import__(modname, fromlist='dummy')
        imp.reload(module)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
                plugin = obj(self)
                self.plugins.append(plugin)

    def loadAllPlugins(self):
        '''
        Load all plugins
        '''
        print('Loading plugins...')
        prefix = plugins.__name__ + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__, prefix):
            del importer
            self.loadPlugin(modname)

    def reloadPlugins(self):
        '''
        Reload all plugins (unload -> load)
        '''
        print('Reloading plugins...')
        self.unloadPlugins()
        self.loadAllPlugins()
        self.registerNotify('notifytextmessage', self.messageFindCommand)

    # notifiy and event functions
    def worker(self):
        while True:
            self.Lock.acquire()
            RegisteredNotifys = self.RegisteredNotifys
            LastCommand = self.LastCommand
            self.Lock.release()
            if len(RegisteredNotifys) == 0 and not self.notifyAllactivated:
                continue
            if LastCommand < time.time() - 180:
                self.command('version')
                self.Lock.acquire()
                self.LastCommand = time.time()
                self.Lock.release()
            telnetResponse = self.telnet.read_until('\n'.encode(), 0.1).decode('utf-8')
            if telnetResponse.startswith('notify'):
                notifyName = telnetResponse.split(' ')[0]
                '''
                ParsedInfo = self.TSRegex.findall(telnetResponse)
                notifyData = {}
                for ParsedInfoKey in ParsedInfo:
                    escaped = self.escapeString(ParsedInfoKey[1])
                    print(escaped)
                    notifyData[ParsedInfoKey[0]] = self.escapeString(escaped)
                '''
                notifyData = self.parseInfo(telnetResponse)
                if self.notifyAllactivated:
                    self.notifyAll_func(notifyName, notifyData)
                    continue
                for RegisteredNotify in RegisteredNotifys:
                    if RegisteredNotify['notify'] == notifyName:
                        RegisteredNotify['func'](notifyName, notifyData)
            time.sleep(0.2)

    # start function (start the bot working)
    def start(self):
        '''
        Load plugins, register events and start main loop
        '''

        self.loadAllPlugins()

        #self.registerEvent('textserver')
        self.registerEvent('textchannel')
        self.registerEvent('textprivate')
        self.registerEvent('server')

        self.registerNotify('notifytextmessage', self.messageFindCommand)

        # start mainloop
        print('Waiting for events...')
        while True:
            time.sleep(0.5)
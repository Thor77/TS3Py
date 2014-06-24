from ts3py import TS3Query
from ts3py import TS3Error
from plugin import Plugin
import plugins
import ts3utils
import time

import imp
import inspect
import pkgutil

class TS3Bot(TS3Query):

    def __init__(self, ip, port, call='!'):
        TS3Query.__init__(self, ip, port)
        self.registeredNotifys = []
        self.registeredEvents = {}
        self.registeredCommands = {}
        self.loopDelay = 0.5
        self.plugins = []
        self.call = call
        self.timeSinceLastCommand = 0
        self.waiting = False

    def servernotifyregister(self, event):
        '''
        Register a notify
        '''
        avail_events = ['server', 'channel', 'textserver', 'textchannel', 'textprivate']
        if event not in avail_events:
            raise TS3Error('Invalid event!')
        self.command('servernotifyregister', {'event': event})
        self.registeredNotifys.append(event)

    def servernotifyunregister(self):
        '''
        Unregister all notifys
        '''
        if len(self.notifyRegistered) > 0:
            self.command('servernotifyunregister')

    def registerEvent(self, eventname, func):
        '''
        Register an event
        '''
        if eventname in self.registeredEvents:
            if len(self.registeredEvents[eventname]) > 0:
                self.registeredEvents[eventname].append(func)
            else:
                self.registeredEvents[eventname] = [func]
        else:
            self.registeredEvents[eventname] = [func]

    def unregisterEvent(self, func):
        '''
        Unregister an event
        '''
        for event in self.registeredEvents:
            if func in self.registeredEvents[event]:
                self.registeredEvents.remove(func)
                return
        raise TS3Error('Cant find event with this func!')

    def unregisterAllEvents(self):
        '''
        Unregister all events
        '''
        self.registeredEvents = {}

    def registerCommand(self, cmd, func, helpstring):
        '''
        Register a command
        '''
        if cmd not in self.registeredCommands:
            self.registeredCommands[cmd] = [func, helpstring]

    def unregisterCommand(self, cmd):
        '''
        Unregister a command
        '''
        if cmd in self.registeredCommands:
            del self.registeredCommands[cmd]

    def unregisterAllCommands(self):
        '''
        Unregister all commands
        '''
        self.registeredCommands = {}

    def loadPlugin(self, modname):
        '''
        Load plugin
        '''
        module = __import__(modname, fromlist='dummy')
        imp.reload(module)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Plugin):
                plugin = obj(self)
                self.plugins.append(plugin)

    def loadPlugins(self):
        '''
        Load all plugins
        '''
        prefix = plugins.__name__ + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__, prefix):
            del importer
            self.loadPlugin(modname)

    def unloadPlugins(self):
        '''
        Unload all plugins
        '''
        self.unregisterAllCommands()
        self.unregisterAllEvents()
        self.servernotifyunregister()
        for plugin in self.plugins:
            plugin.unload()
        self.plugins = []

    def reloadPlugins(self):
        '''
        Reload plugins
        '''
        self.unloadPlugins()
        self.registerDefaults()
        self.loadPlugins()

    def findCommand(self, data):
        '''
        Search for a command -> execute it
        '''
        msg = data['msg'].strip()
        # find
        if msg[:len(self.call)] == self.call:
            command = msg[len(self.call):].split(' ')[0]
            params = msg.split(' ')[1:]
            # execute
            if command in self.registeredCommands:
                self.registeredCommands[command][0](params, data['invokerid'], data['invokername'])

    def registerDefaults(self):
        '''
        Register defaults, the bot need to work correctly
        '''
        # register notifys
        self.servernotifyregister('server')
        self.servernotifyregister('textserver')
        self.servernotifyregister('textchannel')
        self.servernotifyregister('textprivate')
        print('registered notifys')

        # register events
        self.registerEvent('notifytextmessage', self.findCommand)
        print('registered events...')     

    def start(self):
        '''
        Register notifys & events and start the main-loop
        '''
        # register defaults
        self.registerDefaults()
        # load plugins
        self.loadPlugins()
        # start main loop
        print('starting...')
        self.startLoop()

    def startLoop(self):
        while True:
            self.listen()

    def listen(self):
        if self.timeSinceLastCommand < time.time() - 180:
            self.command('version')
            self.timeSinceLastCommand = time.time()
        # event loop
        response = '!=notify'
        while response[:6] != 'notify':
            if not self.waiting:
                response = self.telnet.read_until('\n\r'.encode()).decode('UTF-8', 'ignore').strip()
        notify_name = response.split(' ')[0].strip()
        data = response.replace('%s ' % notify_name, '', 1)
        parsed = ts3utils.parseData(data)
        if notify_name in self.registeredEvents:
            functions = self.registeredEvents[notify_name]
            for func in functions:
                func(parsed)
        time.sleep(self.loopDelay)

    # overwrite command-function
    def command(self, cmd, params={}, options=[]):
        self.timeSinceLastCommand = time.time()
        self.waiting = True
        response = TS3Query.command(self, cmd, params, options)
        self.waiting = False
        return response
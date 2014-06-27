from ts3py import TS3Query
from ts3py import TS3Error
from plugin import Plugin
import plugins
import ts3utils
import time
import sys

from threading import Thread, Event

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
        self.awaitingReponse = False
        self.timeout = 0.2

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
        if len(self.registeredNotifys) > 0:
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
            self.registeredCommands[cmd.lower()] = [func, helpstring]

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

    def loadPlugin(self, pkgname):
        '''
        Load plugin
        '''
        package = __import__(pkgname, fromlist='dummy')
        imp.reload(package)
        for name, obj in inspect.getmembers(package):
            if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
                plugin = obj(self)
                self.plugins.append(plugin)
                break

    def loadPlugins(self):
        '''
        Load all plugins
        '''
        plugindir = 'plugins'
        parent = __import__(plugindir)
        prefix = plugins.__name__ + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(parent.__path__, prefix):
            del importer
            if ispkg:
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
            command = msg[len(self.call):].split(' ')[0].lower()
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
            try:
                self.listen()
            except KeyboardInterrupt:
                self.quit()

    def listen(self):
        if self.timeSinceLastCommand < time.time() - 180:
            self.command('version')
            self.timeSinceLastCommand = time.time()
        # event loop
        response = '!=notify'
        while response[:6] != 'notify':
            if not self.awaitingReponse:
                response = self.telnet.read_until('\n\r'.encode(), self.timeout).decode('UTF-8', 'ignore').strip()
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
        self.awaitingReponse = True
        time.sleep(self.timeout + 0.05)
        response = TS3Query.command(self, cmd, params, options)
        self.awaitingReponse = False
        return response

    def quit(self):
        print('exit')
        self.unloadPlugins()
        sys.exit(1)

class FuncThread(Thread):
    '''
    Useful if you want to run a function every x seconds
    function => function
    x seconds => delay
    '''

    def __init__(self, function, delay):
        Thread.__init__(self)
        self.event = Event()
        self.function = function
        self.delay = delay
        self.daemon = True

    def run(self):
        while not self.event.wait(self.delay):
            self.function()

    def stop(self):
        self.event.set()
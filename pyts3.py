#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the \"Software\"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import telnetlib
import re
import _thread
import time

import imp
import pkgutil
import inspect
import plugins
from plugin import Plugin

class TS3Error(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "ID %s (%s)" % (self.code, self.msg)


class TS3Bot():
    TSRegex = re.compile(r"(\w+)=(.*?)(\s|$|\|)")

    def __init__(self, ip='127.0.0.1', query=10011, call='!'):
        """
        This class contains functions to connecting a TS3 Query Port and send
        command.
        @param ip: IP adress of the TS3 Server
        @type ip: str
        @param query: Query Port of the TS3 Server. Default 10011
        @type query: int
        """
        self.IP = ip
        self.Query = int(query)
        self.Timeout = 5.0
        self.ts3_escape = [
        (chr(92), r'\\'), # \
        (chr(47), r"\/"), # /
        (chr(32), r'\s'), # Space
        (chr(124), r'\p'), # |
        (chr(7), r'\a'), # Bell
        (chr(8), r'\b'), # Backspace
        (chr(12), r'\f'), # Formfeed
        (chr(10), r'\n'), # Newline
        (chr(13), r'\r'), # Carrage Return
        (chr(9), r'\t'), # Horizontal Tab
        (chr(11), r'\v'), # Vertical tab
        ]
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

    def connect(self):
        """
        Open a link to the Teamspeak 3 query port
        @return: A tulpe with a error code. Example: ('error', 0, 'ok')
        """
        try:
            self.telnet = telnetlib.Telnet(self.IP, self.Query)
        except telnetlib.socket.error:
            raise TS3Error(10, 'Can not open a link on the port or IP')
        output = self.telnet.read_until('TS3'.encode(), self.Timeout)
        if output.endswith('TS3'.encode()) == False:
            raise TS3Error(20, 'This is not a Teamspeak 3 Server')
        else:
            return True

    def disconnect(self):
        """
        Close the link to the Teamspeak 3 query port
        @return: ('error', 0, 'ok')
        """
        self.telnet.write('quit \n')
        self.telnet.close()
        return True

    def escapeString(self, value):
        """
        Escape a value into a TS3 compatible string

        @param value: Value
        @type value: string/int
        """

        if isinstance(value, int):
            return str(value)
        
        for i, j in self.ts3_escape:
            value = value.replace(i, j)
        
        return value

    def unescapeString(self, value):
        """
        Unescape a TS3 compatible string into a normal string

        @param value: Value
        @type value: string/int

        """

        if isinstance(value, int):
            return str(value)
        
        for i, j in self.ts3_escape:
            value = value.replace(j, i)
        
        return value

    def command(self, cmd, parameter={}, option=[]):
        """
        Send a command with paramters and options to the TS3 Query.
        @param cmd: The command who wants to send.
        @type cmd: str
        @param parameter: A dict with paramters and value.
        Example: sid=2 --> {'sid':'2'}
        @type cmd: dict
        @param option: A list with options. Example: –uid --> ['uid']
        @type option: list
        @return: The answer of the server as tulpe with error code and message.
        """
        telnetCMD = cmd
        for key in parameter:
            telnetCMD += " %s=%s" % (key, self.escapeString(parameter[key]))
        for i in option:
            telnetCMD += " -%s" % (i)
        telnetCMD += '\n'
        self.telnet.write(telnetCMD.encode())

        telnetResponse = self.telnet.read_until("msg=ok".encode(), self.Timeout)
        telnetResponse = telnetResponse.decode()
        telnetResponse = telnetResponse.split(r'error id=')
        notParsedCMDStatus = "id=" + telnetResponse[1]
        notParsedInfo = telnetResponse[0].split('|')

        if (cmd.endswith("list") == True) or (len(notParsedInfo) > 1):
            returnInfo = []
            for notParsedInfoLine in notParsedInfo:
                ParsedInfo = self.TSRegex.findall(notParsedInfoLine)
                ParsedInfoDict = {}
                for ParsedInfoKey in ParsedInfo:
                    ParsedInfoDict[ParsedInfoKey[0]] = self.unescapeString(
                        ParsedInfoKey[1])
                returnInfo.append(ParsedInfoDict)

        else:
            returnInfo = {}
            ParsedInfo = self.TSRegex.findall(notParsedInfo[0])
            for ParsedInfoKey in ParsedInfo:
                returnInfo[ParsedInfoKey[0]] = self.unescapeString(
                    ParsedInfoKey[1])

        ReturnCMDStatus = {}
        ParsedCMDStatus = self.TSRegex.findall(notParsedCMDStatus)
        for ParsedCMDStatusLine in ParsedCMDStatus:
            ReturnCMDStatus[ParsedCMDStatusLine[0]] = self.unescapeString(
                ParsedCMDStatusLine[1])
        if ReturnCMDStatus['id'] != '0':
            raise TS3Error(ReturnCMDStatus['id'], ReturnCMDStatus['msg'])

        return returnInfo

    # select virtual server
    def use(self, virtualserver):
        '''
        Send use-cmd to the server
        '''
        return self.command('use %s' % virtualserver)

    # login
    def login(self, username, password):
        '''
        Login to the server
        '''
        return self.command('login %s %s' % (username, password))

    # virtualserverlist
    def getServerlist(self):
        '''
        Return dict {id : name}
        '''
        serverlist = {}
        raw = self.command('serverlist', option=['all'])
        for server in raw:
            serverlist[server['virtualserver_id']] = server['virtualserver_name']
        return serverlist

    # channellist
    def getChannellist(self):
        '''
        Return dict {id : name}
        '''
        channellist = {}
        raw = self.command('channellist')
        for channel in raw:
            channellist[channel['cid']] = channel['channel_name']
        return channellist

    # clientlist
    def getClientlist(self):
        '''
        Return dict {id : name}
        '''
        clientlist = {}
        raw = self.command('clientlist')
        for client in raw:
            if client['client_type'] == '0':
                clientlist[client['clid']] = client['client_nickname']
        return clientlist

    # clientinformation
    def getClientinfo(self, client_id):
        '''
        Return a dict with information about client with id client_id
        '''
        return self.command('clientinfo', {'clid': client_id})

    # msgs/poke
    def sendTextmessageServer(self, target_id, msg):
        '''
        Send textmessage to server with id target_id
        '''
        self.command('sendtextmessage', {'targetmode': 3, 'target': target_id, 'msg': msg})

    def sendTextmessageChannel(self, target_id, msg):
        '''
        Send textmessage to channel with id target_id
        '''
        self.command('sendtextmessage', {'targetmode': 2, 'target': target_id, 'msg': msg})

    def sendTextmessageClient(self, target_id, msg):
        '''
        Send textmessage to client with id target_id
        '''
        self.command('sendtextmessage', {'targetmode': 1, 'target': target_id, 'msg': msg})

    def poke(self, target_id, msg):
        '''
        Poke client target_id with msg
        '''
        self.command('clientpoke', {'clid': target_id, 'msg': msg})

    # kick
    def kickFromChannel(self, target_id, reason=None):
        '''
        Kick client target_id with msg from the channel
        '''
        params = {}
        params['clid'] = target_id
        params['reasonid'] = 4
        if reason != None:
            params['reasonmsg'] = reason
        self.command('clientkick', params)

    def kickFromServer(self, target_id, reason=None):
        '''
        Kick client target_id with msg from the server
        '''
        params = {}
        params['clid'] = target_id
        params['reasonid'] = 5
        if reason != None:
            params['reasonmsg'] = reason
        self.command('clientkick', params)

    # channel functions
    def createChannel(self, channel_name, channel_topic=None):
        '''
        Create channel channel_name [with topic channel_topic]
        '''
        params = {}
        params['channel_name'] = channel_name
        if channel_topic != None:
            params['channel_topic'] = channel_topic
        self.command('channelcreate', params)

    def deleteChannel(self, channel_id, force=1):
        '''
        Delete channel with id channel_id (if force == 1, all channels will be moved to the main-channel)
        '''
        self.command('channeldelete', {'cid': channel_id, 'force': force})

    # move client
    def move(self, client_id, channel_id, channel_pw=None):
        '''
        Move client with client_id to channel_id
        '''
        params = {}
        params['clid'] = client_id
        params['cid'] = channel_id
        if channel_pw != None:
            params['cpw'] = channel_pw
        self.command('clientmove', params)

    # ban
    def ban(self, client_id, time_sec=None, reason=None):
        '''
        Ban client with id client_id [for time with reason]
        If time not set, ban will be permanent
        '''
        params = {}
        params['clid'] = client_id
        if time_sec != None:
            params['time'] = time_sec
        if reason != None:
            params['banreason'] = reason
        self.command('banclient', params)

    def deleteBan(self, ban_id):
        '''
        Delete ban with id ban_id
        '''
        self.command('bandel', {'banid': ban_id})

    def deleteAllBans(self):
        '''
        Delete all bans
        '''
        self.command('bandelall')

    def getBanlist(self):
        '''
        Get all active bans on this virtual server
        '''
        raw = self.command('banlist')
        bans = {}
        for ban in raw:
            bans[ban['banid']] = [ban['ip'], ban['created'], ban['invokername'], ban['invokercldbid'], ban['invokeruid'], ban['reason'], ban['enforcements']]

    # self editing
    def changeSelfNick(self, new_name):
        self.command('clientupdate', {'client_nickname': new_name})

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
            params = msg.split(' ')[1:]
            self.gotCommand(msg[len(self.call):], params, data['invokerid'], data['invokername'])

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
            telnetResponse = self.unescapeString(telnetResponse)
            if telnetResponse.startswith('notify'):
                notifyName = telnetResponse.split(' ')[0]
                ParsedInfo = self.TSRegex.findall(telnetResponse)
                #print(ParsedInfo)
                #print(telnetResponse)
                notifyData = {}
                for ParsedInfoKey in ParsedInfo:
                    notifyData[ParsedInfoKey[0]] = self.escapeString(
                        ParsedInfoKey[1])
                if self.notifyAllactivated:
                    self.notifyAll_func(notifyName, notifyData)
                    continue
                for RegisteredNotify in RegisteredNotifys:
                    if RegisteredNotify['notify'] == notifyName:
                        RegisteredNotify['func'](notifyName, notifyData)
            time.sleep(0.2)

    def registerNotify(self, notify, func):
        notify2func = {'notify': notify, 'func': func}

        self.Lock.acquire()
        self.RegisteredNotifys.append(notify2func)
        self.LastCommand = time.time()
        self.Lock.release()

    def unregisterNotify(self, notify, func):
        notify2func = {'notify': notify, 'func': func}

        self.Lock.acquire()
        self.RegisteredNotifys.remove(notify2func)
        self.LastCommand = time.time()
        self.Lock.release()

    def unregisterAllNotifys(self):
        self.RegisteredNotifys = []

    def notifyAll(self, func):
        self.Lock.acquire()

        self.notifyAllactivated = True
        self.notifyAll_func = func

        self.LastCommand = time.time()
        self.Lock.release()

    def registerEvent(self, eventName, parameter={}, option=[]):
        parameter['event'] = eventName
        self.RegisteredEvents.append(eventName)
        self.command('servernotifyregister', parameter, option)
        self.Lock.acquire()
        self.LastCommand = time.time()
        self.Lock.release()

    def unregisterEvent(self):
        self.command('servernotifyunregister')

    # start function (start the bot working)
    def startLoop(self):
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
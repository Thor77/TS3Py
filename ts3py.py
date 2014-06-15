#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the \'Software\'),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED \'AS IS\', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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

class TS3Error(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'ID %s (%s)' % (self.code, self.msg)


class TS3Query:
    TSRegex = re.compile(r'(\w+)=(.*?)(\s|$|\|)')

    def __init__(self, ip='127.0.0.1', query=10011):
        '''
        This class contains functions to connecting a TS3 Query Port and send
        command.
        @param ip: IP adress of the TS3 Server
        @type ip: str
        @param query: Query Port of the TS3 Server. Default 10011
        @type query: int
        '''
        self.IP = ip
        self.Query = int(query)
        self.Timeout = 5.0

        # escape
        self.ts3_escape = [
        (chr(92), r'\\'), # \
        (chr(47), r'\/'), # /
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

    def connect(self):
        '''
        Open a link to the Teamspeak 3 query port
        @return: A tulpe with a error code. Example: ('error', 0, 'ok')
        '''
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
        '''
        Close the link to the Teamspeak 3 query port
        @return: ('error', 0, 'ok')
        '''
        self.telnet.write('quit \n')
        self.telnet.close()
        return True

    def escapeString(self, value):
        '''
        Escape a value into a TS3 compatible string

        @param value: Value
        @type value: string/int
        '''

        if isinstance(value, int):
            return str(value)
        
        for i, j in self.ts3_escape:
            value = value.replace(i, j)
        
        return value

    def unescapeString(self, value):
        '''
        Unescape a TS3 compatible string into a normal string

        @param value: Value
        @type value: string/int

        '''

        if isinstance(value, int):
            return str(value)
        
        for i, j in self.ts3_escape:
            value = value.replace(j, i)
        
        return value

    def command(self, cmd, parameter={}, option=[]):
        '''
        Send a command with paramters and options to the TS3 Query.
        @param cmd: The command who wants to send.
        @type cmd: str
        @param parameter: A dict with paramters and value.
        Example: sid=2 --> {'sid':'2'}
        @type cmd: dict
        @param option: A list with options. Example: –uid --> ['uid']
        @type option: list
        @return: The answer of the server as tulpe with error code and message.
        '''
        telnetCMD = cmd
        for key in parameter:
            telnetCMD += ' %s=%s' % (key, self.escapeString(parameter[key]))
        for i in option:
            telnetCMD += ' -%s' % (i)
        telnetCMD += '\n'
        self.telnet.write(telnetCMD.encode())

        telnetResponse = self.telnet.read_until('msg=ok'.encode(), self.Timeout)
        telnetResponse = telnetResponse.decode()
        telnetResponse = telnetResponse.split(r'error id=')
        notParsedCMDStatus = 'id=' + telnetResponse[1]
        notParsedInfo = telnetResponse[0]

        returnInfo = self.parseInfo(notParsedInfo)
        status = self.parseStatus(notParsedCMDStatus)
        #print(status)

        return returnInfo

    def parseInfo(self, notParsedInfo):
        # split lines
        notParsedInfo = notParsedInfo.split('|')
        if len(notParsedInfo) > 1:
            returnInfo = []
            for line in notParsedInfo:
                parsed = self.TSRegex.findall(line)
                infoDict = {}
                for key in parsed:
                    infoDict[key[0]] = self.unescapeString(key[1])
                returnInfo.append(infoDict)
        else:
            returnInfo = {}
            parsed = self.TSRegex.findall(notParsedInfo[0])
            for key in parsed:
                returnInfo[key[0]] = self.unescapeString(key[1])

        return returnInfo

    def parseStatus(self, notParsedStatus):
        status = {}
        parsed = self.TSRegex.findall(notParsedStatus)
        for line in parsed:
            status[line[0]] = self.unescapeString(line[1])
        if status['id'] != '0':
            raise TS3Error(status['id'], status['msg'])
        else:
            return status

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

    # notify functions
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

    # event functions
    def registerEvent(self, eventName, parameter={}, option=[]):
        parameter['event'] = eventName
        self.RegisteredEvents.append(eventName)
        self.command('servernotifyregister', parameter, option)
        self.Lock.acquire()
        self.LastCommand = time.time()
        self.Lock.release()

    def unregisterEvent(self):
        self.command('servernotifyunregister')
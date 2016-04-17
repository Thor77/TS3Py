import telnetlib
import re
import time
import ts3utils


class TS3Error(Exception):

    def __init__(self, msg, code=None):
        self.code = code
        self.msg = msg

    def __str__(self):
        if self.code is not None:
            return 'ID %s MSG %s' % (self.code, self.msg)
        else:
            return str(self.msg)


class TS3Response:

    def __init__(self, raw_status, data=None):
        self.checkStatus(raw_status)
        if data is not None:
            self.data = ts3utils.parseData(data)
            self.data_e = True
        else:
            self.data_e = False

    def checkStatus(self, raw_status):
        status = raw_status.replace('error ', '')
        parsed = ts3utils.parseData(status)[0]
        if parsed['id'] != 0:
            print(TS3Error(parsed['msg'], parsed['id']))


class TS3Server:

    def __init__(self, ip, port=10011):
        '''
        This class offers a connection to a TS3Server through Query
        '''
        self.timeout = 5.0
        self.telnet = None

        self.connect(ip, port)

    def connect(self, ip, port=10011):
        '''
        Connect to the Server
        '''
        # connect
        self.telnet = telnetlib.Telnet(ip, port)
        # check
        if self.telnet.read_until('TS3'.encode('UTF-8'), self.timeout)[3:]\
                .decode('UTF-8', 'ignore') == 'TS3':
            raise TS3Error('No Teamspeak3-Server on %s:%s!' % (ip, port))

    def disconnect(self):
        '''
        Disconnect from the Server
        '''
        self.command('quit')
        self.telnet.close()

    def command(self, cmd, params={}, options=[]):
        '''
        Send command to the server
        '''
        # send command
        command = ts3utils.build_command(cmd, params, options)
        self.telnet.write('{}\n\r'.format(command).encode('UTF-8',
                                                          errors='replace'))

        # response
        response_data = None
        response = '!=error'
        lines = []
        while not response.startswith('error'):
            response = self.telnet.read_until('\n\r'.encode('UTF-8'))\
                         .decode('UTF-8', 'ignore').strip()
            lines.append(response)
        status = lines[-1]
        if len(lines) > 1:
            response_data = lines[-2]
        parsed_response = TS3Response(status, response_data)
        if parsed_response.data_e:
            return parsed_response.data
        else:
            return []


class TS3Query(TS3Server):

    def __init__(self, ip, port=10011):
        TS3Server.__init__(self, ip, port)

    def login(self, username, password):
        '''
        Login to the server
        '''
        self.command('login %s %s' % (username, password))

    def use(self, virtualserver_id):
        '''
        Select virtualserver
        '''
        self.command('use', {'sid': virtualserver_id})

    # lists
    def serverlist(self):
        '''
        List all virtual servers {id: infos}
        '''
        raw = self.command('serverlist', options=['all'])
        return_info = {}
        for server in raw:
            virtualserver_id = server['virtualserver_id']
            del server['virtualserver_id']
            return_info[virtualserver_id] = server
        return return_info

    def channellist(self):
        '''
        List all channels on the current virtual server {id: infos}
        '''
        raw = self.command('channellist', options=['topic'])
        return_info = {}
        for channel in raw:
            cid = channel['cid']
            del channel['cid']
            return_info[cid] = channel
        return return_info

    def clientlist(self):
        '''
        List all (not query) clients {id: infos}
        '''
        raw = self.command('clientlist', options=['info', 'country'])
        return_info = {}
        for client in raw:
            if client['client_type'] == 0:
                clid = client['clid']
                del client['clid']
                return_info[clid] = client
        return return_info

    # end of lists
    def clientinfo(self, client_id):
        '''
        Get infos about client with client_id
        '''
        return self.command('clientinfo', {'clid': client_id})[0]

    # sending (msg/poke)
    def sendtextmessageServer(self, target_id, msg):
        '''
        Send textmessage to server with id target_id
        '''
        self.command('sendtextmessage',
                     {'targetmode': 3, 'target': target_id, 'msg': msg})

    def sendtextmessageChannel(self, target_id, msg):
        '''
        Send textmessage to channel with id target_id
        '''
        self.command('sendtextmessage',
                     {'targetmode': 2, 'target': target_id, 'msg': msg})

    def sendtextmessageClient(self, target_id, msg):
        '''
        Send textmessage to client with id target_id
        '''
        self.command('sendtextmessage',
                     {'targetmode': 1, 'target': target_id, 'msg': msg})

    def clientpoke(self, target_id, msg):
        '''
        Poke client with id target_id
        '''
        self.command('clientpoke', {'clid': target_id, 'msg': msg})

    # kick
    def clientkickChannel(self, target_id, reason=None):
        '''
        Kick client target_id [with reason to the main-channel]
        '''
        params = {}
        params['clid'] = target_id
        params['reasonid'] = 4
        if reason is not None:
            params['reasonmsg'] = reason
        self.command('clientkick', params)

    def clientkickServer(self, target_id, reason=None):
        params = {}
        params['clid'] = target_id
        params['reasonid'] = 5
        if reason is not None:
            params['reasonmsg'] = reason
        self.command('clientkick', params)

    # channel
    def channelcreate(self, channel_name, channel_topic=None):
        '''
        Create channel channel_name [with topic channel_topic]
        '''
        params = {}
        params['channel_name'] = channel_name
        if channel_topic is not None:
            params['channel_topic'] = channel_topic
        self.command('channelcreate', params)

    def channeldelete(self, channel_id, force=1):
        '''
        Delete channel with id channel_id
        (if force == 1, all channels will be moved to the main-channel)
        '''
        self.command('channeldelete', {'cid': channel_id, 'force': force})

    def banclient(self, client_id, time_sec=None, reason=None):
        '''
        Ban client with id client_id [for time with reason]
        If time not set, ban will be permanent
        '''
        params = {}
        params['clid'] = client_id
        if time_sec is not None:
            params['time'] = time_sec
        if reason is not None:
            params['banreason'] = reason
        self.command('banclient', params)

    def bandel(self, ban_id):
        '''
        Delete ban with id ban_id
        '''
        self.command('bandel', {'banid': ban_id})

    def bandelall(self):
        '''
        Delete all bans
        '''
        self.command('bandelall')

    def banlist(self):
        '''
        Get all active bans on this virtual server
        '''
        raw = self.command('banlist')
        bans = {}
        for ban in raw:
            banid = ban['banid']
            del ban['banid']
            bans[banid] = ban
        return bans

    def clientupdateNick(self, new_nick):
        '''
        Change self nickname to new_nick
        '''
        self.command('clientupdate', {'client_nickname': new_nick})

    def clientmove(self, clid, cid):
        '''
        Move client <clid> to channel with id <cid>
        '''
        self.command('clientmove', {'clid': clid, 'cid': cid})

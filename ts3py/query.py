import telnetlib

from ts3py import ts3utils


class TS3Error(Exception):

    def __init__(self, msg, error_id):
        '''
        Create a TS3Error-object.

        :param msg: error-message
        :param error_id: error-id
        :type msg: string
        :type error_id: int
        '''
        self.msg = msg
        self.error_id = error_id

    def __str__(self):
        return 'ID %s MSG %s' % (self.error_id, self.msg)


class Query:

    def __init__(self, ip, port=10011):
        '''
        Initiate a connection to a Teamspeak3-Server.

        :param ip: ip of the Teamspeak3-server
        :param port: port of the Teamspeak3-server's query-interface
        :type ip: string
        :type port: int
        '''
        self.timeout = 5.0
        self.telnet = None
        self.connected = False

        self.connect(ip, port)

    def connect(self, ip, port=10011):
        '''
        Connect to a Teamspeak3-Server.

        :param ip: ip of the Teamspeak3-server
        :param port: port of the Teamspeak3-server's query-interface
        :type ip: string
        :type port: int
        '''
        # connect
        self.telnet = telnetlib.Telnet(ip, port)
        # check
        if self.telnet.read_until('TS3'.encode('UTF-8'), self.timeout)[3:]\
                .decode('UTF-8', 'ignore') == 'TS3':
            raise Exception('No Teamspeak3-Server on {}:{}!'.format(ip, port))
        self.connected = True

    def disconnect(self):
        '''
        Disconnect from the Teamspeak3-server.
        '''
        self.command('quit')
        self.telnet.close()
        self.connected = False

    def command(self, cmd, params={}, options=[]):
        '''
        Send a command to the Teamspeak3-server and return the response.

        :param cmd: command
        :param params: parameters appended to the command
        :param options: options appended to the command
        :type cmd: string
        :type params: dict
        :type options: list

        :return: response of the command (if any)
        :rtype: list
        '''
        if not self.connected:
            raise Exception('Not connected')
        # send command
        command = ts3utils.build_command(cmd, params, options)
        self.telnet.write('{}\n\r'.format(command).encode('UTF-8',
                                                          errors='replace'))

        # response
        response = '!=error'
        lines = []
        while not response.startswith('error'):
            response = self.telnet.read_until('\n\r'.encode('UTF-8'))\
                .decode('UTF-8', 'ignore').strip()
            lines.append(response)
        # check status
        error_data = ts3utils.parse_response(lines[-1].replace('error ', ''))
        if error_data[0]['id'] != 0:
            raise TS3Error(error_data[0]['msg'], error_data[0]['id'])

        # response-data
        if len(lines) > 1:
            return ts3utils.parse_response(lines[-2])
        return []

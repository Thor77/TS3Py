import ts3py

import ts3py.objects

from contextlib import contextmanager
from collections import namedtuple

Command = namedtuple('Command', ['cmd', 'params', 'options'])


def build_command(cmd, params={}, options=[]):
    '''
    Shorthand for building a new `ts3py.testing.Command` object with defaults
    '''
    return Command(cmd, params, options)


class Query(ts3py.Query):
    def __init__(self):
        '''
        Query is used for testing commands sent to a Teamspeak3-server
        without requiring one on the network
        '''
        self.sent_commands = []
        self.responses = {}

    def command(self, cmd, params={}, options=[]):
        '''
        Overwrite for the original ts3py.Query.command
        '''
        self.sent_commands.append(Command(cmd, params, options))
        if cmd in self.responses:
            return self.responses.pop(cmd)
        else:
            return []

    @contextmanager
    def assert_sent(self, commands):
        '''
        Assert `commands` are sent in this context

        :param commands: commands asserted to be sent

        :type commands: list
        '''
        try:
            yield self
        finally:
            # assert commands sent
            for command in commands:
                assert command in self.sent_commands
            # cleanup
            self.sent_commands = []

    @contextmanager
    def respond(self, responses, assert_empty=True):
        '''
        Pre-define responses for commands in this context

        :param responses: pre-defined responses for commands
        :param assert_empty: assert all responses are used

        :type responses: dict
        :type assert_empty: bool
        '''
        self.responses = responses
        try:
            yield self
        finally:
            # assert empty
            if assert_empty:
                assert len(self.responses) == 0
            # reset responses
            self.responses = {}


class TestingServer(ts3py.objects.Server):
    def __init__(self):
        self.query = Query()

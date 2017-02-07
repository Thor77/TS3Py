from collections import OrderedDict

import ts3utils

escape_data = {
    # escaped => original
    r'command\snot\sfound': r'command not found'
}

command_data = {
    'clientkick clid=5 reasonid=4 reasonmsg=Go\saway!':
        ('clientkick',
            OrderedDict([('clid', 5), ('reasonid', 4),
                         ('reasonmsg', 'Go away!')]), [])
}

response_data = {
    'id=0 msg=ok': [
        OrderedDict([('id', 0), ('msg', 'ok')])
    ],
    'virtualserver_id=1 virtualserver_clientsonline=5\
     virtualserver_uptime=2096023 virtualserver_name=Test\sServer1\
     virtualserver_machine_id|virtualserver_id=2': [
        OrderedDict([('virtualserver_id', 1),
                    ('virtualserver_clientsonline', 5),
                    ('virtualserver_uptime', 2096023),
                    ('virtualserver_name', 'Test Server1'),
                    ('virtualserver_machine_id', '')]),
        OrderedDict([('virtualserver_id', 2)])],
    'clid=1 client_unique_identifier=TESTING42=': [
        OrderedDict([
            ('clid', 1),
            ('client_unique_identifier', 'TESTING42=')
        ])
    ]
}


def test_escape():
    for escaped, original in escape_data.items():
        assert ts3utils.escape(original) == escaped


def test_unescape():
    for escaped, original in escape_data.items():
        assert ts3utils.unescape(escaped) == original


def test_build_command():
    for built, (cmd, params, options) in command_data.items():
        assert ts3utils.build_command(cmd, params, options) == built


def test_parse_response():
    for response, parsed in response_data.items():
        assert ts3utils.parse_response(response) == parsed

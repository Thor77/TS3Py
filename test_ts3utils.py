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


def test_escape():
    for escaped, original in escape_data.items():
        assert ts3utils.escape(original) == escaped


def test_unescape():
    for escaped, original in escape_data.items():
        assert ts3utils.unescape(escaped) == original


def test_build_command():
    for built, (cmd, params, options) in command_data.items():
        assert ts3utils.build_command(cmd, params, options) == built


def test_unpack_command():
    for built, (cmd, params, options) in command_data.items():
        unpacked = ts3utils.unpack_command(built)
        assert unpacked[0] == cmd
        assert unpacked[1] == params

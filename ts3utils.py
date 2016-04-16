import re

escape_strings = [
        (chr(92), r'\\'),  # \
        (chr(47), r'\/'),  # /
        (chr(32), r'\s'),  # Space
        (chr(124), r'\p'),  # |
        (chr(7), r'\a'),  # Bell
        (chr(8), r'\b'),  # Backspace
        (chr(12), r'\f'),  # Formfeed
        (chr(10), r'\n'),  # Newline
        (chr(13), r'\r'),  # Carrage Return
        (chr(9), r'\t'),  # Horizontal Tab
        (chr(11), r'\v'),  # Vertical tab
]

TSRegex = re.compile(r'(\w+)=(.*?)(\s|$|\|)')


def escape(data):
    '''
    Escape to TS3Query-Format

    :param data: data in default form
    :type data: str
    '''
    data = str(data)
    for normal, ts3 in escape_strings:
        data = data.replace(normal, ts3)
    return data


def unescape(data):
    '''
    Escape to Human-Readable-Format

    :param data: data in escaped form
    :type data: str
    '''
    for normal, ts3 in escape_strings:
        data = data.replace(ts3, normal)

    try:
        data = int(data)
        return data
    except ValueError:
        return data


def build_command(cmd, params={}, options=[]):
    '''
    Build query command-string from cmd, params and options

    :param cmd: command
    :param params: parameters for the command
    :param options: options for the command
    :type cmd: str
    :type params: dict
    :type options: list
    '''
    for key, value in params.items():
        cmd += ' {}={}'.format(key, escape(value))
    for option in options:
        cmd += ' -{}'.format(option)
    return cmd.strip()


def parseData(data):
    '''
    Parse telnet-data to key|value-dict
    '''
    parts = data.split('|')
    parsed = []
    for part in parts:
        d = {}
        regexed = TSRegex.findall(part)
        for key in regexed:
            d[key[0]] = unescape(key[1])
        parsed.append(d)
    return parsed

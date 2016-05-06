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
    (chr(11), r'\v')  # Vertical tab
]


def escape(data):
    '''
    Escape to TS3Query-format.

    :param data: data in normal form
    :type data: str
    '''
    data = str(data)
    for normal, ts3 in escape_strings:
        data = data.replace(normal, ts3)
    return data


def unescape(data):
    '''
    Escape to normal-format.

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
    Build query command-string from cmd, params and options.

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


def parse_response(response):
    '''
    Parse raw response to a list of key-value-dicts.

    :param response: query-response
    :type response: str

    :return: list of parsed objects from response
    :rtype: list
    '''
    raw_objects = response.split('|')
    parsed_objects = []
    for raw_object in raw_objects:
        parsed_object = {}
        for param in raw_object.split():
            if '=' not in param:
                key, value = param, ''
            else:
                param_split = param.split('=')
                key = param_split[0]
                value = param_split[1] if len(param_split) == 2\
                    else '='.join(param_split[1:])
            parsed_object[key] = unescape(value)
        parsed_objects.append(parsed_object)
    return parsed_objects

import ts3utils

escape_data = {
    # escaped => original
    r'command\snot\sfound': r'command not found'
}


def test_escape():
    for escaped, original in escape_data.items():
        assert ts3utils.escape(original) == escaped


def test_unescape():
    for escaped, original in escape_data.items():
        assert ts3utils.unescape(escaped) == original

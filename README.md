TS3Py
=====

A Python TS3-Lib

Installation
==============
1. Use 'pip install ts3py'
2. Clone the repo, use 'python setup.py install'

Example usage
=============
Get channellist:
  
    from pyts3 import TS3Query  
    ip = ''
    port = 00000
    query_login = ''
    query_password = ''
    virtualserver_id = 1
    connection = TS3Query(ip, port)
    connection.connect()
    connection.login(query_login, query_password)
    connection.use(virtualserver_id)
    channellist = connection.getChannellist()
    for channel_id in channellist:
        print('Channel-ID: %s Channel-Name: %s' % (channel_id, channellist[channel_id]))
    
Known Bugs
==========
- Missing documentation
- setup.py doesnt work
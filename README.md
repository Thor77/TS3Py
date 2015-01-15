TS3Py
=====

A Python TS3-Lib

Installation
==============
Clone the repo and use 'python setup.py install'

Example usage
=============
Get channellist:
  
    from ts3py import TS3Query  
    ip = ''
    port = 00000
    query_login = ''
    query_password = ''
    virtualserver_id = 1
    connection = TS3Query(ip, port)
    connection.login(query_login, query_password)
    connection.use(virtualserver_id)
    channellist = connection.channellist()
    for channel_id in channellist:
        print('Channel-ID: %s Channel-Name: %s' % (channel_id, channellist[channel_id]))
    
Known Bugs
==========
- Missing documentation

Todo
====
- Improve plugin system

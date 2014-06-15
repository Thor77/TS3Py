TS3Py
=====

A Python TS3-Lib

You want to build a TS3-Bot with this API?
Look at the bot-branch, i've build a plugin-bot!

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
Missing documentation
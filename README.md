TS3Py
=====

A Python TS3-Lib

"Installation"
==============
- Clone the repo

    git clone https://github.com/Thor77/TS3Py.git
    
- Copy the ts3py.py-file to the location, where you need it
- Be happy

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
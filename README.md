TS3Py
=====

A Python TS3-Lib
The \_\_init\_\_-File
=====================
Example:
  
    from pyts3 import TS3Bot  
    ip = ''
    port = 00000
    query_login = ''
    query_password = ''
    virtualserver_id = 1
    bot = TS3Bot(ip, port)
    bot.connect()
    bot.login(query_login, query_password)
    bot.use(virtualserver_id)
    bot.startLoop()
    
Known Bugs
==========
Missing documentation
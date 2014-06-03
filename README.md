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
    bot.startBot(query_login, query_password, virtualserver_id)
    
Known Bugs
==========
Commands with arguments doesnt work!

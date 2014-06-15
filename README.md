TS3Bot
=====

A TS3-Bot build with my TS3-Query-API, TS3Py (look at the master-branch).

The \_\_init\_\_-File
=====================
Example:
  
    from ts3bot import TS3Bot  
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
.. TS3Py documentation master file, created by
   sphinx-quickstart on Sat Apr 16 19:59:10 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TS3Py's documentation!
=================================

TS3Py is a object-orientated interface to Teamspeak3's query-interface.

Let's take a look::

  >>> s = Server('ts.example.com')
  >>> s.login('serveradmin', 'password')
  >>> s.virtual_servers
  [Server1, Server2]
  >>> s.virtual_servers[0].clients
  [serveradmin from 1.1.1.1:39004, thor77]

.. toctree::
   :maxdepth: 2

   api

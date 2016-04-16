TS3Py
=====
[![Build Status](https://travis-ci.org/Thor77/TS3Py.svg?branch=master)](https://travis-ci.org/Thor77/TS3Py) [![Documentation Status](https://readthedocs.org/projects/ts3py/badge/?version=latest)](http://ts3py.readthedocs.org/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/TS3Py.svg)](https://pypi.python.org/pypi/TS3Py) 

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

TS3Py
=====
[![Build Status](https://travis-ci.org/Thor77/TS3Py.svg?branch=master)](https://travis-ci.org/Thor77/TS3Py) [![Documentation Status](https://readthedocs.org/projects/ts3py/badge/?version=latest)](http://ts3py.readthedocs.org/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/TS3Py.svg)](https://pypi.python.org/pypi/TS3Py)

A Python Teamspeak3-Query Library

Checkout the upcoming version with a completely new API [here](https://github.com/Thor77/TS3Py/tree/develop).

Installation
============
`pip install TS3Py`

Examples
========
```python
from ts3py import Server
s = Server(host='ts.example.com', port=10011)  # connect
s.login('serveradmin', 'password')  # login
vserver = s.virtual_servers[0]  # choose first virtual server
for channel in vserver.channel:  # iterate over channels
  print(channel.cid, channel, sep='|')  # print channelid and channel-data
```

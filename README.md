TS3Py
=====
[![Build Status](https://travis-ci.org/Thor77/TS3Py.svg?branch=master)](https://travis-ci.org/Thor77/TS3Py) [![Documentation Status](https://readthedocs.org/projects/ts3py/badge/?version=latest)](http://ts3py.readthedocs.org/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/TS3Py.svg)](https://pypi.python.org/pypi/TS3Py)

A Python Teamspeak3-Query Library

Installation
============
`pip install TS3Py`

Examples
========
```python
from ts3py import TS3Query
c = TS3Query('ts.example.com')
c.login('serveradmin', 'password')
c.use(1)
channellist = c.channellist()
for channel_id in channellist:
    print(channel_id, channellist[channel_id], sep='|')
c.disconnect()
```

import os
from setuptools import setup

setup(

    name='TS3Py',
    version='0.4.1',
    author='Thor77',
    author_email='thor77@thor77.org',
    description='A Python Teamspeak3-Query Library',
    keywords='ts3 pyts3 ts3py teamspeak teamspeak3',
    url='https://github.com/Thor77/TS3py',
    long_description='''
.. image:: https://travis-ci.org/Thor77/TS3Py.svg?branch=master
    :target: https://travis-ci.org/Thor77/TS3Py

.. image:: https://readthedocs.org/projects/ts3py/badge/?version=latest
    :target: http://ts3py.readthedocs.org/en/latest/?badge=latest

.. code-block:: python

    from ts3py import TS3Query
    c = TS3Query('ts.example.com')
    c.login('serveradmin', 'password')
    c.use(1)
    channellist = c.channellist()
    for channel_id in channellist:
        print(channel_id, channellist[channel_id], sep='|')
    c.disconnect()
    ''',
    py_modules=['ts3py', 'ts3utils'],

)

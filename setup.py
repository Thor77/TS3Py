import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(

    name = 'TS3Py',
    version = '0.0.1',
    author = 'Thor77',
    author_email = 'thor77@xthor77.tk',
    description = 'A python TS3Query-API',
    keywords = 'ts3 pyts3 ts3py',
    url = 'https://github.com/Thor77/TS3py',
    long_description = read('README.md'),

)
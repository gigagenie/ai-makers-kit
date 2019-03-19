"""
gkit - AI Makers Kit Python Library
"""

__title__ = 'gkit'
__version__ = '0.2.0'
__author__ = 'CheolMin Lee'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018 KT corp.'
VERSION = tuple(map(int, __version__.split('.')))

try:
    from ._drivers import *
except:
    pass
from .kws import *
from .grpc import *

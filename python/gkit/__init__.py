"""
gkit
"""

__title__ = 'gkit'
__version__ = '0.1.0'
__author__ = 'CheolMin Lee'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018 KT corp.'
VERSION = tuple(map(int, __version__.split('.')))

from .common import *
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
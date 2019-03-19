""" read config file: gkit.config """

try:
    # Python 3.x
    from configparser import ConfigParser
except ImportError:
    # Python 2.x
    from ConfigParser import SafeConfigParser as ConfigParser
config = ConfigParser()
config.read('gkit.config')
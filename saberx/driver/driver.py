from saberx.executers.threaddriver import ThreadExecuter
from saberx.actionparser.actionextractor import ActionExtractor
from configparser import SafeConfigParser
import time
import optparse
import os

CONFIG_FILE = "saberx.config"

def drive():
    global CONFIG_FILE

    # parse args
    parser = optparse.OptionParser()
    parser.add_option('-f', action="store", dest="config", help="Config file.")
    options, args = parser.parse_args()

    if options.config:
        CONFIG_FILE = options.config

    config = __load_config()

    if not __sanitize_config():
        '''
            Config is not proper. Issue has been logged. Exiting SaberX
        '''

        exit(2)

def __load_config():
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)

    section = "DEFAULT"
    config = {}

    for param, value in parser.items(section):
        config[param] = value

    return config

def __sanitize_config():

    '''
        sanitize the config and log issues
    '''
    
    return True

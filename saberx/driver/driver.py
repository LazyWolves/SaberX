from saberx.executers.threaddriver import ThreadExecuter
from saberx.actionparser.actionextractor import ActionExtractor
import time
import optparse
import os

CONFIG_FILE = "saberx.config"

def drive():
    # parse args

    parser = optparse.OptionParser()
    parser.add_option('-f', action="store", dest="config", help="Config file.")
    options, args = parser.parse_args()

    if options.config:
        CONFIG_FILE = options.config
    

def __sanitize_config():

    '''
        sanitize the config and log issues
    '''
    
    return True

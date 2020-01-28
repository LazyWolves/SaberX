"""
.. module:: driver
   :synopsis: Main entry point for Saberx

"""

from saberx.executers.threaddriver import ThreadExecuter
from saberx.actionparser.actionextractor import ActionExtractor
from configparser import SafeConfigParser
import time
import optparse
import os
import logging

# global constants used by driver
CONFIG_FILE = "/etc/saberx/saberx.conf"
LOCK_FILE = "saberx.lock"
LOG_FILE = "/var/log/saberx/saberx.log"
SLEEP_PERIOD = 10

def drive():
    """
        **Method for starting Saberx**

        This is the entry point for saberx. It will load the config file
        and the action plan. Spawn threads to execute each group and start
        and continue the state loop.

        Returns:
            None: Returns nothing
    """
    global CONFIG_FILE

    # parse args
    parser = optparse.OptionParser()
    parser.add_option('-f', action="store", dest="config", help="Config file.")
    options, args = parser.parse_args()

    # if config file is provided then load it.
    if options.config:
        CONFIG_FILE = options.config

    config = __load_config()

    if not __sanitize_config(config):
        '''
            Config is not proper. Issue has been logged. Exiting SaberX
        '''

        exit(2)

    logger = __setup_logging(LOG_FILE)

    actionExtractor = ActionExtractor(configpath=config.get("action_plan"), logger=logger)
    if not actionExtractor.action_plan_loaded:

        '''
            Failed to load action plan. Issue has been logged. Exitting SaberX
        '''
        exit(2)

    if not __clear_existing_lock(config.get("lock_dir"), logger):

        '''
            Issue has already been logged. Existting Saberx
        '''
        exit(2)

    # get the sleep time from conf if available
    sleep_period = int(config.get("sleep_period", SLEEP_PERIOD))

    action_groups = actionExtractor.get_action_groups()

    threadExecuter = ThreadExecuter(groups=action_groups, logger=logger)

    while True:

        # threads should be spwaned only if a lock can be aquired.
        if __can_aquire_lock(config.get("lock_dir")):
            logger.info("Proceeding with saberx run")
            worker_and_run_success = threadExecuter.spawn_workers(os.path.join(config.get("lock_dir"), LOCK_FILE))
            if not worker_and_run_success:

                '''
                    Either lock could not be aquired or release failed. Issue has been logged.
                    Exit SaberX
                '''
                exit(2)
            logger.info("Saberx run finished successfully")
        time.sleep(sleep_period)


def __clear_existing_lock(lock_dir, logger):
    """
        **Method for clearing existing lock**

        This method clears any existing lock if present.

        Args:
            lock_dir (string) : Directory where lock file is generated
            logger (logging) : object for logging

        Returns:
            bool : Whether lock could be cleared

    """

    lock_file = os.path.join(lock_dir, LOCK_FILE)

    try:
        if os.path.exists(lock_file):
            os.unlink(lock_file)
        return True
    except Exception as e:

        '''
            Unable to clear stale lock. Log issue. Send false. Stale locks muct be removed
            or else runs wont take place
        '''

        logger.critical("Unable to remove lock file : Exeption : {}".format(str(e)))

        return False

def __can_aquire_lock(lock_dir):
    """
        **Method for checking if lock can be aquired**

        This method checks if lock can be aquired. If can be aquired then
        it returns true, else false.

        Args:
            lock_dir (string) : Directory where lock file is generated

        Returns:
            bool : Whether lock could be aquired

    """

    lock_file = os.path.join(lock_dir, LOCK_FILE)

    if os.path.exists(lock_file):
        return False

    return True

def __load_config():
    """
        **Method for loading config into python dict**

        This method parses the conf file and creates the corresponding python dict

        Returns:
            dict : Whether lock could be cleared

    """

    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)

    section = "DEFAULT"
    config = {}

    for param, value in parser.items(section):
        config[param] = value

    return config

def __sanitize_config(config):

    '''
        sanitize the config and log issues
    '''
    
    return True

def __setup_logging(log_file):
    """
        **Method for setting up logging**

        Takes a log file location and creates a logging object using it

        Args:
            log_file (string) : Path to log file

        Returns:
            logging : logging object

    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(log_file)
    logger_handler.setLevel(logging.DEBUG)
    logger_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                         datefmt='%Y-%m-%d %H:%M:%S')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger

if __name__ == "__main__":
    drive()

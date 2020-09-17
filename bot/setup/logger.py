import logging
from datetime import datetime
import os
import sys

LOG_FILE = './out/logs/' + datetime.now().strftime("%H.%M.%S_%d.%m.%Y") + \
    '_' + os.getenv('AD_USERNAME') + '.log'

def configure():
    """
    Setup the logger to output to file and console
    """
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.INFO)
    rootLogger.warning('ALL OUTPUT IS IN UTC TIME')
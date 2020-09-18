import logging
from datetime import datetime
import os
import sys

LOG_FILE = './out/logs/' + datetime.now().strftime("%Y.%m.%d_%H.%M.%S_") + \
    os.getenv('AD_USERNAME') + '.log'

def configure_logger():
    """
    Setup logger to output to file and console
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
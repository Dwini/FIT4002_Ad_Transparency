import requests
import os
import logging
from pathlib import Path

import setup

LOGGER = logging.getLogger()
LOGS_BASE_URL = 'https://fit4002.s3-ap-southeast-2.amazonaws.com/logs/'

def log_error_to_db(message):
    """
    Log app crash to db
    """
    p = Path(LOGGER.handlers[0].baseFilename)

    url = os.getenv('DB_URL') + '/errors'
    data = {
        'log_file': p.name,
        'message': message,
        'link': LOGS_BASE_URL + p.name
    }
    r = requests.post(url, data=data)
    r.raise_for_status()

def handle_error(error):
    """
    Error handler for main app
    """
    message = None

    if setup.TIMED_OUT:
        message = 'Program timed out'
        LOGGER.error(message)
    else:
        message = str(error)
        LOGGER.error('Exception occurred', exc_info=True)

    if os.getenv('UPLOAD_LOGS') == "1":
        log_error_to_db(message)
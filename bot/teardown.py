import os
import logging
import requests

LOGGER = logging.getLogger()

def teardown(session, display):
    LOGGER.info('Performing teardown')

    if session is not None:
        session.quit()

    if display is not None:
        display.stop()

    # Upload log file
    print('Uploading log file')
    if os.getenv('UPLOAD_LOGS') == "1":
        url = os.getenv('DB_URL') + '/logs'
        log_file = open(LOGGER.handlers[0].baseFilename, 'rb')
        r = requests.post(url, files={ 'file':  log_file })
        r.raise_for_status()
import os
import logging
import requests

LOGGER = logging.getLogger()

def teardown(session, display):
    print('>> Performing teardown')

    if session is not None:
        session.quit()

    if display is not None:
        display.stop()

    logfile_path = LOGGER.handlers[0].baseFilename
    print('>> Log file saved to: ' + logfile_path)

    # Upload log file
    if os.getenv('UPLOAD_LOGS') == "1":
        print('>> Uploading log file')

        url = os.getenv('DB_URL') + '/logs'
        logfile = open(logfile_path, 'rb')
        r = requests.post(url, files={ 'file':  logfile })
        r.raise_for_status()
# import external libraries.
import os, logging, requests
from dotenv import load_dotenv
load_dotenv()   # load env variables.

log = logging.getLogger()

def teardown(session=None):
    log.info('>> Performing teardown')

    if session is not None:
        session.quit()

    logfile_path = log.handlers[0].baseFilename
    log.info('>> Log file saved to: ' + logfile_path)

    # Upload log file
    if os.getenv('UPLOAD_LOGS') == "1":
        log.info('>> Uploading log file')

        url = os.getenv('DB_URL') + '/logs'
        with open(logfile_path, 'rb') as logfile:
            r = requests.post(url, files={ 'file':  logfile })

        r.raise_for_status()

import os
import logging
import zipfile
import shutil

log = logging.getLogger()

ALL_SESSIONS_PATH = './out/sessions/'
SESSION_PATH = ALL_SESSIONS_PATH + os.getenv('AD_USERNAME')
INITIAL_SESSION_PATH = './driver/initial_sessions/' + os.getenv('AD_USERNAME') + '.zip'

def get_session(delete_old=False):
    """
    If session data exists this will extract the related zip file
    """
    if os.path.isdir(SESSION_PATH):
        if delete_old:
            log.info('Removing old session data')
            shutil.rmtree(SESSION_PATH, ignore_errors=True)
        else:
            log.info('Session data already exists. No need to extract')
            return

    if not os.path.isfile(INITIAL_SESSION_PATH):
        log.warning('No inital session data found, new session data will be created')
        return

    log.info('Extracting session data')
    zipfile.ZipFile(INITIAL_SESSION_PATH, 'r').extractall(ALL_SESSIONS_PATH)
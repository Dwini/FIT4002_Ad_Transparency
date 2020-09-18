import logging
from time import sleep
import requests
import os

LOGGER = logging.getLogger()

def ping_db():
    # Do not execute until db container has been started.
    response = None
    attempts = 0

    while response is None and attempts < 10:
        attempts += 1
        try:
            response = requests.get(os.getenv('DB_URL')+'/heartbeat')
            LOGGER.info('Found db project')
        except:
            LOGGER.warning('No response from db project. attempt: '+str(attempts))
            sleep(10)
            pass

    if attempts >= 10: # if no response. break.
        raise RuntimeError('Could not connect to db project')
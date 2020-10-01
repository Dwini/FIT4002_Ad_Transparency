import signal 
import logging
from pyvirtualdisplay import Display
from pathlib import Path
import os
import sys

from setup.logger import configure_logger
from setup.database import ping_db

log = logging.getLogger()
TIMED_OUT = False

def check_env():
    """
    Check all required environment variables have been set
    """
    env_vars = [
        'AD_USERNAME',
        'DB_URL',
        'NUM_TERMS',
        'USE_PROXIES',
        'CHANGE_LOCATION',
        'UPLOAD_LOGS'
    ]
    
    for v in env_vars:
        if os.getenv(v) is None:
            raise NameError('%s environment variable has not been set' % v)

def create_dirs():
    Path('./out').mkdir(exist_ok=True)
    Path('./out/sessions').mkdir(exist_ok=True)
    Path('./out/logs').mkdir(exist_ok=True)

def timeout_action(_signo, _stack_frame):
    """
    Action to be performed when timeout is detected
    """
    global TIMED_OUT
    TIMED_OUT = True
    log.error('Program timed out')
    raise TimeoutError()

def start_display():
    """
    Setup for container builds.
    If this is running in a container, import and create a virtual display
    """
    display = Display(visible=0, size=(800, 600))
    display.start()
    return display

def initial_setup():
    check_env()
    create_dirs()
    configure_logger()

    # For container builds
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        signal.signal(signal.SIGALRM, timeout_action)
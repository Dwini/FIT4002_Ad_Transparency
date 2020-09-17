from pathlib import Path
import logging

LOGGER = logging.getLogger()

def create_dirs():
    LOGGER.info('Creating output directories')
    
    Path('./out').mkdir(exist_ok=True)

    Path('./out/profiles').mkdir(exist_ok=True)
    Path('./out/logs').mkdir(exist_ok=True)
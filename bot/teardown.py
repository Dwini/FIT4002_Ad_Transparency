import logging

LOGGER = logging.getLogger()

def teardown(session, display):
    LOGGER.info('Performing teardown')

    if session is not None:
        session.quit()

    if display is not None:
        display.stop()
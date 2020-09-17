# import external libraries.
import os
import sys
import random
from time import sleep
import os
import requests
import logging

# local imports
import setup
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad

# get environment variables.
AD_USERNAME = os.getenv('AD_USERNAME') or "mwest5078"   # arbitrary default bot.
DB_URL = os.getenv('DB_URL') or "http://localhost:8080"
NUM_TERMS = 3               # number of terms to search

def main():
    setup.configure_logger()
    setup.create_dirs()

    LOGGER = logging.getLogger()

    # TODO: Could move this into its own file
    # Do not execute until db container has been started.
    response = None
    attempts = 0
    while response is None and attempts < 10:
        attempts += 1
        try:
            response = requests.get(DB_URL+'/heartbeat')
            LOGGER.info('Found db project')
        except:
            LOGGER.warning('No response from db project. attempt: '+str(attempts))
            sleep(10)
            pass
    if attempts >= 10: # if no response. break.
        LOGGER.error('Could not connect to db project')
        return

    # TODO: Could also move this under setup
    # if this is running in the container, import and create virtual display.
    container_build = False
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()

    LOGGER.info('Using bot: ' + AD_USERNAME)

    bot = None
    creating = False
    if creating:
        bot = botCreator()
    else:
        bot = Bot(AD_USERNAME)

    # MAIN SESSION/BROWSING START
    session = setup.get_driver()
    setup.set_location(session, bot.position)

    # start scraping
    ws = webscraper(session, bot)

    try:
        ws.activate_bot()
    except:
        LOGGER.exception('Pre-login searching failed')
        raise

    ws.login()

    # Example youtube scraping
    yt_scraper = youtube_scraper(session, bot, yt_ad.ALL)
    lista = ['dropshipping ','free money how']
    for items in lista:
        yt_scraper.scrape_youtube_video_ads(items)
    
    LOGGER.info('Session complete. Quitting...')
    session.quit()

    # close display if in container.
    if container_build == True:
        display.stop()

if __name__ == '__main__':
    # print('Environment Vars: username='+str(AD_USERNAME)+' proxies='+str(USE_PROXIES)+' location='+str(CHANGE_LOCATION))
    main()

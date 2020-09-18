# import external libraries.
import os
import sys
import random
from time import sleep
import os
import requests
import logging
from dotenv import load_dotenv

# local imports
import setup
from teardown import teardown
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad

# get environment variables.
load_dotenv()
AD_USERNAME = os.getenv('AD_USERNAME') or "mwest5078"   # arbitrary default bot.

def main():
    setup.configure_logger()
    LOGGER = logging.getLogger()
    session = None
    display = None          # For container builds

    try:
        setup.create_dirs()
        setup.ping_db()

        # For container builds
        if len(sys.argv) > 1 and sys.argv[1] == '-c':
            display = setup.start_display()

        bot = None
        creating = False
        if creating:
            bot = botCreator()
        else:
            bot = Bot(AD_USERNAME)

        session = setup.get_driver()

        if os.getenv('CHANGE_LOCATION') == "1":
            setup.set_location(session, bot.position)

        # Google scraping
        ws = webscraper(session, bot)

        ws.activate_bot()
        ws.login()

        # Youtube scraping
        yt_scraper = youtube_scraper(session, bot, yt_ad.ALL)
        for items in bot.search_terms:
            yt_scraper.scrape_youtube_video_ads(items)
    except:
        LOGGER.exception('Something went wrong. Possible bug')
        raise
    else:
        LOGGER.info('Session completed successfully')
    finally:
        teardown(session, display)

if __name__ == '__main__':
    # print('Environment Vars: username='+str(AD_USERNAME)+' proxies='+str(USE_PROXIES)+' location='+str(CHANGE_LOCATION))
    main()

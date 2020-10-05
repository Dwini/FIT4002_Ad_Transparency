# import external libraries.
import os
import sys
import random
from time import sleep
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

# local imports
import setup
from driver import get_driver
from errors import handle_error
from teardown import teardown
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad

# get environment variables.
AD_USERNAME = os.getenv('AD_USERNAME') or "mwest5078"   # arbitrary default bot.

def main():
    setup.initial_setup()

    log = logging.getLogger()
    session = None
    display = None          # For container builds

    try:
        setup.ping_db()

        # For container builds
        if len(sys.argv) > 1 and sys.argv[1] == '-c':
            display = setup.start_display()

        # Init bot
        bot = None
        creating = False
        if creating:
            bot = botCreator()
        else:
            bot = Bot(AD_USERNAME)

        # Driver setup
        session = get_driver(bot.position)

        # Mark bot as running
        bot.updateStatus('Running')
        
        # Google scraping
        ws = webscraper(session, bot)
        ws.activate_bot()

        ws.login()

        # Youtube scraping
        yt_scraper = youtube_scraper(session, bot, yt_ad.ALL)
        for items in bot.search_terms:
            yt_scraper.scrape_youtube_video_ads(items)
    except Exception as e:
        handle_error(e)
        bot.updateStatus('Crashed')
    else:
        log.info('Session completed successfully')
        bot.updateStatus('Idle')
    finally:
        teardown(session, display)

def example_create_bot():
    import requests, json
    url = os.getenv('DB_URL') + '/bot/test'     # 'test' is bots username. Don't need to send with data
    data = { 
        'password':  'test123123',
        'name': 'test',
        'DOB': 'test',
        'gender': 'test',
        'political_ranking': 0,
        'other_terms_category': 0,
        'location': {
            'latitude': 0,
            'longitude': 0
        }
    }
    r = requests.post(url, json=data)       # Need to send as json or won't work
    r.raise_for_status()

if __name__ == '__main__':
    example_create_bot()
    # main()

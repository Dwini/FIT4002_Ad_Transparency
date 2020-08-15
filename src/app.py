import sys
from random import uniform
from time import sleep
import os

# local imports
from database import Database
import proxy
import config_driver
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad


def main():
    container_build = False

    # if this is running in the container, import and create virtual display.
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()
    
    # initialise db
    db = Database()

    creating = False
    if creating:
        newBot = botCreator()
    else:
        bots = db.fetch_all_items('Bots')

        for bot in bots:
            # todo: remove to use all bots. this is only for testing
            if bot['username'] != "mwest5078":
                continue

            print('>> Using bot: ' + bot['username'])

            # define location of bot
            pos = { 'lat': uniform(-90, 90), 'lon': uniform(-180, 180) }
            if 'location' in bot:
                pos = {
                    'lat': float(bot['location']['latitude']),
                    'lon': float(bot['location']['longitude'])
                }

            session = None
            if os.environ['USE_PROXIES'] == "1":
                session = config_driver.setup_driver_with_proxy(pos)
                if session is None:
                    print(">> Quitting")
            else:
                # ... or use this to setup without proxy
                session = config_driver.setup_driver()

            # change location
            config_driver.set_location(session, pos)

            # start scraping
            webscraper(session, bot, db)

            # start google scraping
            # webscraper.login(bot, session)
            # webscraper.setup_profile(bot, session, db)
            # webscraper.scrape_google_ads(bot, session, db)

            # start youtube scraping
            # yt_scraper = youtube_scraper(session, yt_ad.ALL)
            # yt_scraper.scrape_youtube_video_ads('reopen economy')


    # close display if in container.
    if container_build == True:
        display.stop()


if __name__ == '__main__':
    main()
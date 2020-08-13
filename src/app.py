# import external libraries.
import os
import sys
from random import uniform
from time import sleep

# local imports
from database import Database
import proxy
import webscraper
import config_driver
from youtube_scraper import youtube_scraper, yt_ad

# get environment variable.
AD_USERNAME = os.environ['AD_USERNAME']

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

    # get bots
    bots = db.fetch_all_items('Bots')

    for bot in bots:
        # todo: remove to use all bots. this is only for testing
        if bot['username'] != AD_USERNAME:
            continue

        # todo: remove this as well. only for testing
        bot['search_terms'] = ['domain names']

        print('using bot: ' + bot['username'])

        # define location of bot
        pos = None
        if 'location' in bot:
            pos = {
                'lat': float(bot['location']['latitude']),
                'lon': float(bot['location']['longitude'])
            }
        else:
            # default pos to completely random position
            pos = { 'lat': uniform(-90, 90), 'lon': uniform(-180, 180) }

        # use this to setup driver with a list of possible proxies
        # todo: move this into its own function somewhere?
        for p in proxy.get_closest_proxies(pos):
            print("trying proxy: %s..." % p, end='')
            session = config_driver.setup_driver(p)

            if proxy.ip_check(session):
                print("proxy is working")
                break

            print("failed")
            session.quit()

        # ... or use this to setup without proxy
        # session = config_driver.setup_driver()

        # change location
        config_driver.set_location(session, pos)

        # start google scraping
        webscraper.login(bot, session)
        webscraper.setup_profile(bot, session, db)
        webscraper.scrape_google_ads(bot, session, db)

        # start youtube scraping
        yt_scraper = youtube_scraper(session, yt_ad.ALL)
        yt_scraper.scrape_youtube_video_ads('reopen economy')


    # close display if in container.
    if container_build == True:
        display.stop()

if __name__ == '__main__':
    print(AD_USERNAME)
    main()

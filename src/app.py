import sys
from random import uniform

# local imports
from database import Database
import proxy
import webscraper
import config_driver


def main():
    container_build = False

    # if this is running in the container, import and create virtual display.
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()
    
    db = Database()

    bots = db.fetch_all_items('Bots')

    for bot in bots:
        # todo: remove to use all bots. this is only for testing
        if bot['username'] != "jw1083888":
            continue

        print('using bot: ' + bot['username'])

        # define location of bot
        pos = None
        if 'location' in bot:
            pos = {
                'lat': float(bot['location']['latitude']),
                'lon': float(bot['location']['longitude'])
            }
        else:
            # default pos to random position
            pos = { 'lat': uniform(-90, 90), 'lon': uniform(-180, 180) }

        # use this to setup driver with proxy that is closest
        # proxyIP = proxy.get_closest_proxy(pos)
        # session = config_driver.setup_driver(proxyIP)
        # proxy.ip_check(session)

        # use this to setup driver without proxy
        session = config_driver.setup_driver()
        
        # change location
        config_driver.set_location(session, pos)

        # start scraping
        webscraper.login(bot, session)
        webscraper.setup_profile(bot, session, db)
        webscraper.scrape_google_ads(bot, session, db)

    # close display if in container.
    if container_build == True:
        display.stop()


if __name__ == '__main__':
    main()
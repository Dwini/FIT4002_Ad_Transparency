# import external libraries.
import os
import sys
from random import uniform
from time import sleep
import os
import requests

# local imports
import proxy
import config_driver
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad

# get environment variables.
USE_PROXIES = os.getenv('USE_PROXIES') or "0"
CHANGE_LOCATION = os.getenv('CHANGE_LOCATION') or "0"
AD_USERNAME = os.getenv('AD_USERNAME') or "mwest5078"   # arbitrary default bot.
DB_URL = os.getenv('DB_URL') or "http://localhost:8080"

def examples():
    ### start example ###
    # this is an exmaple of how to create an ad with a
    # file (using adLinks.txt file in this folder)
    files = { 'file': open('adLinks.txt', 'rb') }
    values = { 'bot': 'test', 'link': 'test', 'headline': 'test' }
    r = requests.post(DB_URL+'/ads', files=files, data=values)
    r.raise_for_status()
    ### end example ###


def main():
    # Do not execute until db container has been started.
    response = None
    attempts = 0
    while response is None and attempts < 10:
        attempts += 1
        try:
            response = requests.get(DB_URL+'/heartbeat')
            print('found db container...')
        except:
            print('no response from container. attempt: '+str(attempts))
            sleep(10)
            pass

    # if no response. break.
    if attempts >= 10:
        return

    container_build = False

    # if this is running in the container, import and create virtual display.
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        container_build = True
        from pyvirtualdisplay import Display

        # set xvfb display since there is no GUI in container.
        display = Display(visible=0, size=(800, 600))
        display.start()

    bots = []
    creating = False
    if creating:
        newBot = botCreator()
    else:
        r = requests.get(DB_URL+'/bots')
        r.raise_for_status()
        bots = r.json()

    for b in bots:
        if b['username'] != AD_USERNAME:
            continue

        print('>> Using bot: ' + b['username'])

        # define location of bot
        pos = { 'lat': uniform(-90, 90), 'lon': uniform(-180, 180) }
        if 'location' in b:
            pos = {
                'lat': float(b['location']['latitude']),
                'lon': float(b['location']['longitude'])
            }

        search_terms = ['trump']
        if 'political_ranking' in b:
            url = DB_URL + '/search_terms/political/%d' % b['political_ranking']
            r = requests.get(url)
            r.raise_for_status()
            search_terms = r.json()

        bot = Bot(
            firstname=b['name'][0],
            lastname= b['name'][1],
            username=b['username'],
            password=b['password'],
            gender=b['gender'],
            birthDay=b['DOB'][:2],
            birthMonth=b['DOB'][3:5],
            birthYear=b['DOB'][6:],
            politicalStance=b['political_ranking'],
            search_terms=search_terms,
            profileBuilt=True
        )

        session = None
        if USE_PROXIES == "1":
            session = config_driver.setup_driver_with_proxy(pos)
            if session is None:
                print(">> Quitting")
                return
        else:
            # ... or use this to setup without proxy
            session = config_driver.setup_driver()

        # change location
        if CHANGE_LOCATION == "1":
            config_driver.set_location(session, pos)

        # start scraping
        webscraper(session, bot)

        # start google scraping
        # webscraper.login(bot, session)
        # webscraper.setup_profile(bot, session)
        # webscraper.scrape_google_ads(bot, session)

        # start youtube scraping
        # yt_scraper = youtube_scraper(session, yt_ad.ALL)
        # yt_scraper.scrape_youtube_video_ads('reopen economy')

        print(">> Session complete")


    # close display if in container.
    if container_build == True:
        display.stop()

if __name__ == '__main__':
    print(AD_USERNAME)
    main()

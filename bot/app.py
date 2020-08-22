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

# get environment variable.
AD_USERNAME = os.environ['AD_USERNAME']

def examples():
    ### start example ###
    # this is an exmaple of how to create an ad with a 
    # file (using adLinks.txt file in this folder)
    files = { 'file': open('adLinks.txt', 'rb') }
    values = { 'bot': 'test', 'link': 'test', 'headline': 'test' }
    r = requests.post('http://db:8080/ads', files=files, data=values)
    r.raise_for_status()
    ### end example ###


def main():
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
        r = requests.get('http://db:8080/bots')
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
            r = requests.get('http://db:8080/search_terms')
            r.raise_for_status()
            search_terms = r.json()[b['political_ranking']]

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
        if os.environ['USE_PROXIES'] == "1":
            session = config_driver.setup_driver_with_proxy(pos)
            if session is None:
                print(">> Quitting")
        else:
            # ... or use this to setup without proxy
            session = config_driver.setup_driver()

        # change location
        if os.environ['CHANGE_LOCATION'] == "1":
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

# import external libraries.
import os
import sys
import random
from time import sleep
import os
import requests

# local imports
import setup.driver as setup_driver
import setup.files as setup_files
import setup.location as setup_location
from bot import Bot
from webscraper import webscraper
from signup import botCreator
from youtube_scraper import youtube_scraper, yt_ad

# get environment variables.
CHANGE_LOCATION = os.getenv('CHANGE_LOCATION') == "1"
AD_USERNAME = os.getenv('AD_USERNAME') or "mwest5078"   # arbitrary default bot.
DB_URL = os.getenv('DB_URL') or "http://localhost:8080"
NUM_TERMS = 3               # number of terms to search

def main():
    # Do not execute until db container has been started.
    response = None
    attempts = 0
    while response is None and attempts < 10:
        attempts += 1
        try:
            response = requests.get(DB_URL+'/heartbeat')
            print('found db project...')
        except:
            print('no response from db project. attempt: '+str(attempts))
            sleep(10)
            pass

    # if no response. break.
    if attempts >= 10:
        return

        
    print("---START SESSION---")

    setup_files.create_output_dirs()

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
        pos = { 'lat': random.uniform(-90, 90), 'lon': random.uniform(-180, 180) }
        if 'location' in b:
            pos = {
                'lat': float(b['location']['latitude']),
                'lon': float(b['location']['longitude'])
            }

        # Get political search terms
        url = DB_URL + '/search_terms/political/%d' % b['political_ranking']
        r = requests.get(url)
        r.raise_for_status()
        search_terms = r.json()

        # Get other search terms
        url = DB_URL + '/search_terms/other/%d' % b['other_terms_category']
        r = requests.get(url)
        r.raise_for_status()
        search_terms = search_terms + r.json()

        random.shuffle(search_terms)
        random.shuffle(search_terms)
        random.shuffle(search_terms)
        search_terms = search_terms[:NUM_TERMS]

        bot = Bot(firstname=b['name'][0],
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

        # MAIN SESSION/BROWSING START

        session = setup_driver.get_driver()

        if session is None:
            print(">> Quitting")
            return

        # change location
        if CHANGE_LOCATION:
            setup_location.set_location(session, pos)

        # start scraping
        ws = webscraper(session, bot)

        try:
            ws.activate_bot()
        except:
            print('>> ERROR: Initial searching failed')

        ws.login()

        # Example youtube scraping
        yt_scraper = youtube_scraper(session, bot, yt_ad.ALL)
        lista = ['dropshipping ','free money how']
        for items in lista:
            yt_scraper.scrape_youtube_video_ads(items)
        
        if session:
            session.quit()

    print("---END SESSION---")

    # close display if in container.
    if container_build == True:
        display.stop()

if __name__ == '__main__':
    # print('Environment Vars: username='+str(AD_USERNAME)+' proxies='+str(USE_PROXIES)+' location='+str(CHANGE_LOCATION))
    main()

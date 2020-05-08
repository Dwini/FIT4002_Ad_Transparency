import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep

from config import keys
from config import settings
from database import Database

class bot:
    def __init__(self, id, name, username, password, status):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.status = status

def get_bots(db):
    # Code to get the bots from the database
    response = db.get_all_bots()
    bots = []

    for entry in response:
        bots.append(bot(entry['id'], entry['name'], entry['username'], entry['password'], entry['status']))

    return bots

def login(bot, webdriver):
    # Login
    webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
    sleep(2)
    webdriver.find_element_by_id('identifierId').send_keys(bot.username + "@gmail.com")
    webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    sleep(4)
    webdriver.find_element_by_css_selector("input[type=password]").send_keys(bot.password)
    webdriver.find_element_by_id('passwordNext').click()
    sleep(2)

def setup_profile(bot, webdriver, db):
    # Get Keywords
    keywords = pd.read_csv(bot.status + '_keywords.csv', index_col=None, header=0)
    # Go through all keywords
    sleep(1)
    links = []
    for keyword in keywords.Keyword:
        url = 'http://www.google.com/'
        # Search Keyword using text box
        webdriver.get(url)
        sleep(2)
        search_box = webdriver.find_element_by_xpath("//input[@name='q']")
        search_box.send_keys(keyword)
        sleep(2)
        search_box.send_keys(Keys.RETURN)
        sleep(6)
        # wait until shows result
        results = webdriver.find_elements_by_css_selector('div.g')

        # save site visit to database
        db.log_action(bot.id, url, ['search'], keyword)

        try:
            for _ in range(2):
                new = True
                link = results[_].find_element_by_tag_name("a")
                href = link.get_attribute("href")
                for link in links:
                 if href == link:
                     new = False
                if new:
                    links.append(href)
        except:
            print()
    for link in links:
        try:
            webdriver.get(link)

            # save site visit to database
            db.log_action(bot.id, link, ['visit'])

            sleep(10)
        except:
            print()


def scrape_google_ads(bot, webdriver, db):
    session = HTMLSession()

    ad_list = [] #empty list to store ad details

    # Get Keywords
    keywords = pd.read_csv(bot.status + '_keywords.csv', index_col =None, header=0 )
    # Go through all keywords
    sleep(1)
    for keyword in keywords.Keyword:
        webdriver.get('https://google.com/search?q=' + keyword)
        r = session.get('https://google.com/search?q=' + keyword)
        sleep(10)
        # Get the 4 ads at the top
        ads = r.html.find('.ads-ad')

        for ad in ads:
            ad_link = ad.find('.V0MxL', first=True).absolute_links #link to landing page
            ad_link = next(iter(ad_link)) #need this since the result from above is set
            ad_headline = ad.find('h3.sA5rQ', first=True).text #headline of the ad
            ad_copy = ad.find('.ads-creative', first=True).text #ad copy
            ad_list.append([keyword, ad_link, ad_headline, ad_copy]) #append data row to list

            # save ad to database
            db.save_ad(bot.id, ad_link, ad_headline, ad_copy)



    df_ads = pd.DataFrame(ad_list, columns = ['keyword', 'ad_link', 'ad_headline', 'ad_copy'])

    #timestamp so we dont overwrite old CSVs
    ts = time.time()
    #write out to CSV for reference
    df_ads.to_csv('top-ads-'+str(ts)+'.csv')

    #Selenium loop thru dataframe to save PNGs into "screenshots" folder
    for index, row in df_ads.iterrows():
        print('Index: ' + str(index) + ', Ad Link: ' + row['ad_link'])
        webdriver.get(row['ad_link'])

        # save site visit to database
        db.log_action(bot.id, row['ad_link'], ['visit'])

        sleep(2)
        webdriver.save_screenshot('screenshots/'+str(index)+'.png')
        #webdriver.get_screenshot_as_file(str(index) + '.png')

    webdriver.quit()

if __name__ == "__main__":
    db = Database()
    bots = get_bots(db)
    #bots.append(bot('Phill', 'phillfranco44@gmail.com', 'pF1234()', 'democrat'))
    #bots.append(bot('Phill', 'phillfranco44@gmail.com', 'pF1234()', 'democrat'))

    for bot in bots:
        if settings.BROWSER == "chrome":
            # Open chrome
            session = webdriver.Chrome(ChromeDriverManager().install())
        elif settings.BROWSER == "firefox":
            # Open firefox
            session = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        login(bot, session)
        setup_profile(bot, session, db)
        scrape_google_ads(bot, session, db)

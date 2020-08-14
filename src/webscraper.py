import pandas as pd
import time
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep

from config import keys
from database import Database

def login(bot, webdriver):
    # Login
    print('logging into Google account...', end="")

    webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
    sleep(2)
    webdriver.find_element_by_id('identifierId').send_keys(bot['username'])
    webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    sleep(4)
    webdriver.find_element_by_css_selector("input[type=password]").send_keys(bot['password'])
    webdriver.find_element_by_id('passwordNext').click()
    sleep(2)

    print("success")

"""
Setup a bots profile by searching Google for 
given search terms and then visiting sites

bot: bot dictionary
webdriver: the selenium driver
db: datbase instance
"""
def setup_profile(bot, webdriver, db):
    print('seting up profile')
    num_links_to_visit = 2

    # Get Keywords
    # keywords = pd.read_csv(bot.status + '_keywords.csv', index_col=None, header=0)
    keywords = bot['search_terms']

    # Go through all keywords
    sleep(1)
    links = []
    for keyword in keywords:
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
        db.log_action({ 
            "bot": bot['username'], 
            "url": url, 
            "actions": ['search'], 
            "search_term": keyword 
        })

        try:
            for _ in range(num_links_to_visit):
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
            db.log_action({ 
                "bot": bot['username'], 
                "url": link, 
                "actions": ['visit']
            })

            sleep(10)
        except:
            print()

"""
Scrape Google ads from given searches and
visit each scraped ad

bot: bot dictionary
webdriver: the selenium driver
db: datbase instance
"""
def scrape_google_ads(bot, webdriver, db):
    print('scraping google ads...')
    session = HTMLSession()

    ad_list = [] #empty list to store ad details

    # Get Keywords
    # keywords = pd.read_csv(bot.status + '_keywords.csv', index_col =None, header=0 )
    keywords = bot['search_terms']

    # Go through all keywords
    sleep(1)
    for keyword in keywords:
        webdriver.get('https://google.com/search?q=' + keyword)
        r = session.get('https://google.com/search?q=' + keyword)
        sleep(10)

        # Get the 4 ads at the top
        ads = r.html.find('.ads-fr')

        for ad in ads:
            ad_link = ad.find('.Krnil', first=True).absolute_links #link to landing page
            ad_link = next(iter(ad_link)) #need this since the result from above is set
            ad_headline = ad.find('div.cfxYMc', first=True).text #headline of the ad
            ad_copy = ad.find('.MUxGbd', first=True).text #ad copy
            ad_list.append([keyword, ad_link, ad_headline, ad_copy]) #append data row to list

            print(ad.find('.MUxGbd'))
            # save ad to database
            db.save_ad({
                "bot": bot['username'], 
                "link": ad_link, 
                "headline": ad_headline, 
                "html": ad_copy
            })

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
        db.log_action({ 
            "bot": bot['username'], 
            "url": row['ad_link'], 
            "actions": ['visit']
        })

        sleep(2)
        webdriver.save_screenshot('screenshots/'+str(index)+'.png')
        #webdriver.get_screenshot_as_file(str(index) + '.png')

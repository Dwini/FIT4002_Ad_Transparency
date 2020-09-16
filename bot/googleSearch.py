# import external libraries.
import os
import pandas as pd
import time
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep
import requests
from website_traverse import webTraverse
from traversal_functions import random_wait_and_scroll
from random import randint

# import local modules.
from bot import Bot

# define constants
DB_URL = os.getenv('DB_URL') or "http://localhost:8080"

class googleSearch:
    def __init__(self, webdriver, bot, scrapping):
        """
        :param webdriver: the driver for the selenium project
        :param videoAds: enable saving of youtube video Ads, defaults to false
        :param sidebarAds: enable saving of youtube sidebar Ads, defaults to false
        :param videoAds: enable saving of youtube video Ads, defaults to false
        """
        self.webdriver = webdriver
        self.bot = bot
        self.scrapping = scrapping
        self.ads = []  # can be refactored into dictionary, as right now only contains the html element



    def search_keywords(self, num_links_to_visit=2):
        #print('seting up profile')

        # this sections is for collecting Ads
        session = HTMLSession()
        ad_list = []  # empty list to store ad details

        # Get Keywords
        keywords = self.bot.getSearchTerms()

        # Go through all keywords
        sleep(1)
        links = []
        for keyword in keywords:
            url = 'http://www.google.com/'
            # Search Keyword using text box
            self.webdriver.get(url)
            self.webdriver.get(url)
            sleep(2)
            try:
                search_box = self.webdriver.find_element_by_xpath("//input[@name='q']")
                search_box.send_keys(keyword)
                sleep(2)
                search_box.send_keys(Keys.RETURN)
            except:
                print("Couldn't find google search box, skipping... ")

            try:
                r = session.get('https://google.com/search?q=' + keyword) # For collecting ads
            except:
                print("Could not connect to Google, trying again... ")

            sleep(randint(8, 10))

            if self.scrapping:
                self.scrape(self, ad_list, keyword, r)
            # wait until shows result
            results = self.webdriver.find_elements_by_css_selector('div.g')

            # save site visit to database
            r = requests.post(DB_URL+'/logs', data={
                "bot": self.bot.getUsername(),
                "url": url,
                "actions": ['search'],
                "search_term": keyword
            })
            r.raise_for_status()

            newLinks = []
            #gather new links
            try:
                for _ in range(num_links_to_visit):
                    new = True
                    link = results[_].find_element_by_tag_name("a")
                    href = link.get_attribute("href")
                    newLinks.append(href,)
                    for link in links:
                        if href == link:
                            new = False
                    if new:
                        links.append(href)
            except:
                print("Could not access links on google search page, skipping... ")

            random_wait_and_scroll(self.webdriver)

            #pick random link
            link_to_visit = randint(0,len(newLinks)-1)

            self.visit_website(newLinks[link_to_visit])

        if self.scrapping:
            df_ads = pd.DataFrame(ad_list, columns=['keyword', 'ad_link', 'ad_headline', 'ad_copy'])

            # timestamp so we dont overwrite old CSVs
            ts = time.time()

            # write out to CSV for reference
            df_ads.to_csv('top-ads-' + str(ts) + '.csv')

            # todo: save to database instead
            # Selenium loop thru dataframe to save PNGs into "screenshots" folder
            for index, row in df_ads.iterrows():
                print('Index: ' + str(index) + ', Ad Link: ' + row['ad_link'])
                self.webdriver.get(row['ad_link'])

                # save site visit to database
                r = requests.post(DB_URL+'/logs', data={
                    "bot": self.bot.getUsername(),
                    "url": row['ad_link'],
                    "actions": ['visit']
                })
                r.raise_for_status()

                sleep(2)
                self.webdriver.save_screenshot('screenshots/' + str(index) + '.png')
                # webdriver.get_screenshot_as_file(str(index) + '.png')


    def visit_website(self, link):

        try:
            print('Clicked a search result...')
            wt = webTraverse(self.webdriver, self.bot, True)
            randDepth = randint(1,3)
            wt.traverse(urls=[link], traverseDepth=randDepth)
        except:
            print("Failed to vist: %s" % link)

    def scrape(self, ad_list, keyword, r):
        # Get the 4 ads at the top
        ads = r.html.find('.ads-ad')
        for ad in ads:
            ad_link = ad.find('.V0MxL', first=True).absolute_links  # link to landing page
            ad_link = next(iter(ad_link))  # need this since the result from above is set
            ad_headline = ad.find('h3.sA5rQ', first=True).text  # headline of the ad
            ad_copy = ad.find('.ads-creative', first=True).text  # ad copy
            ad_list.append([keyword, ad_link, ad_headline, ad_copy])  # append data row to list

            # save ad to database
            r = requests.post(DB_URL + '/ads', data={
                "bot": self.bot.getUsername(),
                "link": ad_link,
                "headline": ad_headline,
                "html": ad_copy
            })
            r.raise_for_status()

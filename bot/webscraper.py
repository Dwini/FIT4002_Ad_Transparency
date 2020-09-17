import pandas as pd
import time
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep
import random
import logging

from youtube_scraper import youtube_scraper
from googleSearch import googleSearch

LOGGER = logging.getLogger()

class webscraper:
    def __init__(self, webdriver, bot, scrapping = False):
        self.webdriver = webdriver
        self.bot = bot
        self.scrapping = scrapping

        #self.login()
        #self.activate_bot()

    def handle_captcha(self):
        """
        Saves a screenshot of the captcha (out/captcha.png) and reads from
        file (out/captcha) the captcha text to input
        """
        self.webdriver.save_screenshot('./out/captcha.png')
        sleep(20)

        with open('./out/captcha', 'r') as f:
            self.webdriver.find_element_by_xpath("//input[@aria-label='Type the text you hear or see']").send_keys(f.read())
        
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())

    def login(self):
        LOGGER.info('Logging into Google account')

        self.webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(2)

        try:
            self.webdriver.find_element_by_id('identifierId').send_keys(self.bot.getUsername())
        except:
            LOGGER.warning('Could not find username field. Assuming already logged in')
            self.webdriver.save_screenshot('./out/login_proof.png')
            return

        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        try:
            self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())
        except:
            LOGGER.critical("Captcha encountered!")
            self.handle_captcha()
        
        self.webdriver.find_element_by_id('passwordNext').click()
        sleep(20)   # large wait time as proxies are slow...

        LOGGER.info("Login successful")

    def activate_bot(self):

        #self.login()

        choice = random.randint(0,1)
        if choice == 0:
            LOGGER.info('google searching...')
            gs = googleSearch(self.webdriver, self.bot, self.scrapping)
            gs.search_keywords(num_links_to_visit=1)
        else:
            LOGGER.info('youtube searching')
            youtube_scraper(self.webdriver, self.bot, self.scrapping)

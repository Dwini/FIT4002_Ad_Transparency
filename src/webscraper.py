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

from config import keys
from database import Database

from website_traverse import webTraverse
from youtube_scraper import youtube_scraper
from googleSearch import googleSearch


class webscraper:
    def __init__(self, webdriver, bot, db, scrapping = False):
        self.webdriver = webdriver
        self.bot = bot
        self.db = db
        self.scrapping = scrapping
        self.login()
        self.task_decider()

    def login(self):
        # Login
        print('logging into Google account...', end="")

        self.webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(2)
        self.webdriver.find_element_by_id('identifierId').send_keys(self.bot.getUsername())
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)
        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())
        self.webdriver.find_element_by_id('passwordNext').click()
        sleep(2)

        print("success")

    def task_decider(self):
        choice = random.randint(0,2)
        if choice == 0:
            googleSearch(self.webdriver, self.bot, self.db, self.scrapping)
        elif choice == 1:
            print('good')
            wt = webTraverse(self.webdriver, self.db, self.bot, self.scrapping)
            wt.traverse()

        else:
            youtube_scraper(self.webdriver, self.db, self.scrapping)



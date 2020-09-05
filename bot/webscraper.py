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

from website_traverse import webTraverse
from youtube_scraper import youtube_scraper
from googleSearch import googleSearch


class webscraper:
    def __init__(self, webdriver, bot, scrapping = False):
        self.webdriver = webdriver
        self.bot = bot
        self.scrapping = scrapping
        print('logging in...')
        self.login()
        print('deciding task...')
        self.task_decider()

    def login(self):
        # Login
        print('logging into Google account...', end="")

        self.webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(20)   # large wait time as proxies are slow...
        self.webdriver.find_element_by_id('identifierId').send_keys(self.bot.getUsername())
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(20)   # large wait time as proxies are slow...
        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())
        self.webdriver.find_element_by_id('passwordNext').click()
        sleep(20)   # large wait time as proxies are slow...

        print("success")

    def task_decider(self):
        choice = random.randint(0,2)
        if choice == 0:
            print('google searching...')
            googleSearch(self.webdriver, self.bot, self.scrapping)
        elif choice == 1:
            print('web traversing...')
            wt = webTraverse(self.webdriver, self.bot, self.scrapping)
            wt.traverse()

        else:
            print('youtube searching')
            youtube_scraper(self.webdriver, self.scrapping)

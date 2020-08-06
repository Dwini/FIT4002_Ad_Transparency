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

from website_traverse import website_traverse
from youtube_scrapper import youtube_scrapper

class webscraper:
    def __init__(self, bot, scrapping, webdriver):
        self.bot = bot
        self.scrapping = scrapping
        self.login(webdriver)
        self.task_decider(webdriver)

    def login(self, webdriver):
        # Login
        print('logging into Google account...', end="")

        webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(2)
        webdriver.find_element_by_id('identifierId').send_keys(self.bot.getUsername())
        webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)
        webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())
        webdriver.find_element_by_id('passwordNext').click()
        sleep(2)

        print("success")

    def task_decider(self, webdriver):
        choice = random.randint(0,2)
        if choice == 0:
            website_traverse.traverse(webdriver, bot)
        elif choice == 1:
            website_traverse.traverse(webdriver, bot)
        else:
            youtube_scrapper.traverse(webdriver, bot)



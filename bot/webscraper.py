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

    def handle_captcha(self):
        """
        Saves a screenshot of the captcha (out/captcha.png) and reads from
        file (out/captcha) the captcha text to input
        """
        self.webdriver.save_screenshot('/tmp/out/captcha.png')
        sleep(20)

        with open('/tmp/out/captcha', 'r') as f:
            self.webdriver.find_element_by_xpath("//input[@aria-label='Type the text you hear or see']").send_keys(f.read())
        
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())

    def login(self):
        print('>> Logging into Google account')

        self.webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(2)

        try:
            self.webdriver.find_element_by_id('identifierId').send_keys(self.bot.getUsername())
        except:
            print('\t>> Could not find username field. Assuming already logged in')
            self.webdriver.save_screenshot('/tmp/out/login_proof.png')
            return

        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        try:
            self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())
        except:
            print("\t>> Captcha encountered!")
            self.handle_captcha()
        
        self.webdriver.find_element_by_id('passwordNext').click()
        sleep(20)   # large wait time as proxies are slow...

        print("\t>> Login successful")

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

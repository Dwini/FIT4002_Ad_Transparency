import pandas as pd
import time
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from requests_html import HTMLSession
from time import sleep
import random
import logging

from youtube_scraper import youtube_scraper
from googleSearch import googleSearch

log = logging.getLogger()

class webscraper:
    def __init__(self, webdriver, bot, scrapping = False):
        self.webdriver = webdriver
        self.bot = bot
        self.scrapping = scrapping

    def handle_captcha(self):
        """
        Saves a screenshot of the captcha (out/captcha.png) and reads from
        file (out/captcha) the captcha text to input
        """
        self.webdriver.save_screenshot('./out/captcha.png')
        sleep(20)

        with open('./out/captcha', 'r') as f:
            try:
                self.webdriver.find_element_by_xpath("//input[@aria-label='Type the text you hear or see']").send_keys(f.read())
            except:
                log.error('Captcha input failed. Possibly incorrect captcha?')
                raise
        
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())

    def login(self):
        log.info('Logging into Google account')

        url = 'https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/'
        log.info('Opening ' + url)
        actions_email = ActionChains(self.webdriver)
        actions_password = ActionChains(self.webdriver)
        actions_enter = ActionChains(self.webdriver)

        self.webdriver.get(url)
        sleep(2)
        self.webdriver.save_screenshot('./out/login0.png')

        try:
            log.info('Entering username')
            actions_email = actions_email.send_keys(self.bot.getUsername())
            actions_email.perform()
            sleep(5)
        except:
            log.warning('Could not find username field. Assuming already logged in')
            return

        actions_enter = actions_enter.send_keys(Keys.ENTER)
        actions_enter.perform()
        sleep(7)
        self.webdriver.save_screenshot('./out/login1.png')

        try:
            log.info('Entering password')
            actions_password = actions_password.send_keys(self.bot.getPassword())
            actions_password.perform()
            sleep(4)
        except:
            log.critical('Captcha encountered!')
            log.info('Waiting for user input')
            self.handle_captcha()
        
        actions_enter.perform()
        self.webdriver.save_screenshot('./out/login2.png')
        sleep(5)   # large wait time as proxies are slow...

        log.info("Login successful")

        url = 'https://mail.google.com/mail/u/0/#inbox'
        self.webdriver.get(url)
        sleep(2)
        self.webdriver.save_screenshot('./out/login_proof.png')

    def activate_bot(self):
        choice = random.randint(0,1)
        if choice == 0:
            log.info('Pre-login Google searching')
            gs = googleSearch(self.webdriver, self.bot, self.scrapping)
            gs.search_keywords(num_links_to_visit=1)
        else:
            log.info('Pre-login Youtube searching')
            youtube_scraper(self.webdriver, self.bot, self.scrapping)

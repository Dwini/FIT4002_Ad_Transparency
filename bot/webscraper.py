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


from youtube_scraper import youtube_scraper
from googleSearch import googleSearch


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
        self.webdriver.save_screenshot('/tmp/out/captcha.png')
        sleep(20)

        with open('/tmp/out/captcha', 'r') as f:
            self.webdriver.find_element_by_xpath("//input[@aria-label='Type the text you hear or see']").send_keys(f.read())
        
        self.webdriver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)

        self.webdriver.find_element_by_css_selector("input[type=password]").send_keys(self.bot.getPassword())

    def login(self):
        print('>> Logging into Google account')

        actions_email = ActionChains(webdriver)
        actions_password = ActionChains(webdriver)
        actions_enter = ActionChains(webdriver)

        self.webdriver.get('https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/')
        sleep(2)

        try:
            actions_email = actions_email.send_keys('Joel.Trump.3546@gmail.com')
            actions_email.perform()
            sleep(5)
        except:
            print('\t>> Could not find username field. Assuming already logged in')
            self.webdriver.save_screenshot('/tmp/out/login_proof.png')
            return

        actions_enter = actions_enter.send_keys(Keys.ENTER)
        actions_enter.perform()
        sleep(7)

        try:
            actions_password = actions_password.send_keys('hi1234()')
            actions_password.perform()
            sleep(4)
        except:
            print("\t>> Captcha encountered!")
            self.handle_captcha()
        
        actions_enter.perform()
        sleep(20)   # large wait time as proxies are slow...

        print("\t>> Login successful")

    def activate_bot(self):

        #self.login()

        choice = random.randint(0,1)
        if choice == 0:
            print('google searching...')
            gs = googleSearch(self.webdriver, self.bot, self.scrapping)
            gs.search_keywords(num_links_to_visit=1)
        else:
            print('youtube searching')
            youtube_scraper(self.webdriver, self.bot, self.scrapping)

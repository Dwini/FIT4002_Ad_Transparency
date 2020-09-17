# import external libraries.
import os
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import logging


# import local modules.
from bot import Bot

# define constants
DB_URL = os.getenv('DB_URL') or "http://localhost:8080"

LOGGER = logging.getLogger()

class joinPoliticalParty:
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


    def join_trump(self):
        url = 'https://www.donaldjtrump.com/'
        self.webdriver.get(url)

        sleep(2)
        try:
            join_btn = self.webdriver.find_element_by_xpath('//*[@id="header-nav-top"]/ul/li[2]/a')
            join_btn.click()
            sleep(4)
            email_btn = self.webdriver.find_element_by_xpath('//*[@id="wrapper"]/main/section/div[1]/div[1]/div/ul/li[2]/a')
            email_btn.click()
        except:
            LOGGER.warning("Couldn't find join page, trying direct url... ")
            url = 'https://www.donaldjtrump.com/get-involved/email'
            self.webdriver.get(url)
        sleep(2)

        try:
            actions_create = ActionChains(self.webdriver)
            email_txtbox = self.webdriver.find_element_by_xpath('// *[ @ id = "ddform_11"]')
            email_txtbox.click()
            actions_create = actions_create.send_keys(self.bot.getUsername())
            actions_create = actions_create.send_keys(Keys.TAB)
            actions_create = actions_create.send_keys(self.bot.getZipcode())
            actions_create = actions_create.send_keys(Keys.ENTER)
            actions_create.perform()

        except:
            LOGGER.warning("Couldn't join Trump, skipping... ")

        # TODO work around hCaptcha

        LOGGER.info("Join Trump successful")


    def join_biden(self):
        url = 'https://joebiden.com/#'
        self.webdriver.get(url)
        sleep(5)
        try:
            popup = self.webdriver.find_element_by_xpath('//*[@id="modal-close"]')
            popup.click()

        except:
            LOGGER.warning("Couldn't close popup, skipping... ")
        sleep(4)

        try:
            actions_create = ActionChains(self.webdriver)
            email_txtbox = self.webdriver.find_element_by_xpath('//*[@id="body"]/footer/section/div[2]/form/div/div[1]')
            email_txtbox.click()
            actions_create = actions_create.send_keys(self.bot.getUsername())
            actions_create = actions_create.send_keys(Keys.TAB)
            actions_create = actions_create.send_keys(self.bot.getZipcode())
            actions_create = actions_create.send_keys(Keys.TAB)
            actions_create = actions_create.send_keys(Keys.TAB)
            actions_create = actions_create.send_keys(Keys.ENTER)
            actions_create.perform()

        except:
            LOGGER.warning("Couldn't join Biden, skipping... ")

        LOGGER.info("Join Biden successful")

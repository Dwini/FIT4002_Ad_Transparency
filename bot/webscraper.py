from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import logging
import os
from website_traverse import webTraverse
from youtube_scraper import youtube_scraper
from googleSearch import googleSearch

log = logging.getLogger()

class webscraper:
    def __init__(self, webdriver, bot, scrapping = False):
        self.webdriver = webdriver
        self.bot = bot
        self.scrapping = scrapping
        self.urls = self.getUrls()

    def getUrls(self):
        political_stance = self.bot.politcalStance

        if political_stance == 0:
            urlsFile = 'urls/left_wing.txt'
        else:
            urlsFile = 'urls/right_wing.txt'

        urls = open(urlsFile, 'r')
        returnUrls = []
        for url in urls:
            returnUrls.append(url)

        random.shuffle(returnUrls)

        return returnUrls

    def nextUrl(self):
        return self.urls.pop()

    def handle_captcha(self):
        """
        DEVELOPMENT ONLY
        Saves a screenshot of the captcha (out/captcha.png) and reads from
        file (out/captcha) the captcha text to input.
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

    def check_login(self):
        log.info('Checking whether login was successful')

        url = 'https://accounts.google.com/login'
        log.info('Opening ' + url)
        self.webdriver.get(url)
        sleep(3)

        # TODO: REMOVE
        self.webdriver.save_screenshot('./out/login2.png')

        if ('myaccount' in self.webdriver.current_url):
            log.info('Login successful')
        else:
            log.warning('Login most likely failed')

    def login(self):
        log.info('Logging into Google account')

        url = 'https://www.google.com/accounts/Login?hl=en&continue=http://www.google.com/'
        log.info('Opening ' + url)
        actions_email = ActionChains(self.webdriver)
        actions_password = ActionChains(self.webdriver)
        actions_enter = ActionChains(self.webdriver)

        self.webdriver.get(url)
        sleep(2)

        log.info('Entering username')
        actions_email = actions_email.send_keys(self.bot.getUsername())
        actions_email.perform()
        sleep(5)

        actions_enter = actions_enter.send_keys(Keys.ENTER)
        actions_enter.perform()
        sleep(7)

        # TODO: REMOVE
        self.webdriver.save_screenshot('./out/login0.png')

        log.info('Entering password')
        actions_password = actions_password.send_keys(self.bot.getPassword())
        actions_password.perform()
        sleep(4)

        actions_enter.perform()
        sleep(5)   # large wait time as proxies are slow...

        # TODO: REMOVE
        self.webdriver.save_screenshot('./out/login1.png')

        self.check_login()

    def activate_bot(self):

        i = int(os.getenv('NUM_TERMS'))
        wt = webTraverse(self.webdriver, self.bot, self.scrapping)


        while i != 0:
            choice = random.randint(0,2)

            sleep(random.uniform(1, 2))
            if choice == 0:
                log.info('Google searching')
                gs = googleSearch(self.webdriver, self.bot, self.scrapping)
                gs.search_keywords(num_links_to_visit=1)
                i -= 1
            elif choice == 1:
                log.info('Youtube searching')
                yt_scraper = youtube_scraper(self.webdriver, self.bot, self.scrapping)

                # perform a youtube search for each keyword.
                for item in self.bot.search_terms:
                    yt_scraper.scrape_youtube_video_ads(item)
            else:
                wt.traverse([self.nextUrl()])


# import exteral libraries.
import os
from google_adsense_scrape import getGoogleAds
from bot import Bot
from random import random, randint
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import base64
import math
import requests
import multiprocessing
import logging

log = logging.getLogger()

"""Methodical traversal or set of websites with scraping if required.

  Use traverse to being traversal

      Attributes:
          driver (obj: WebDriver): To traverse with. MUST be headless for full page screenshots to work
          scrape (Bool): Whether sraping is required .

      """
class webTraverse:

    def __init__(self, driver, bot, scrape=True):

        self.driver = driver
        self.toScrape = scrape
        self.bot = bot

    """Begin traversal or set of websites with scraping if required.


        Attributes:
            urls (List of strings): To traverse with. MUST be headless for full page screenshots to work
            timeout (Int Seconds): When to stop activity. Will complete current direct action.

                """
    def traverse(self, urls, traverseDepth=2):

        if not(urls):
            urls = open('urls.txt', 'r')


        for url in urls:

            log.info('Opening ' + url)
            try:
                self.driver.get(url)
            except:
                log.error("Broken link: %s" % url)
                continue

            log.info('Waiting...')
            sleep(randint(10, 15))

            log.info('Opening ' + url)

            # Logs route deprecated
            # try:
            #     r = requests.post(os.getenv('DB_URL')+'/logs', data={
            #         "bot": self.bot.getUsername(),
            #         "url": url,
            #         "actions": ['visit']
            #     })
            #     r.raise_for_status()
            # #except ConnectionRefusedError:
            # except:
            #     log.error("Couldn't log activity. Connection Error")

            # dialogues can get in the way of ads and scrolling
            self.clear_dialogs()

            self.remove_header()

            self.random_wait_and_scroll()

            if self.toScrape:
                #self.full_page_screenshot(url)
                getGoogleAds(self.driver, self.bot)

            if traverseDepth > 0:
                self.click_local_links(traverseDepth)
                traverseDepth = traverseDepth - 1

            self.random_wait_and_scroll()

    # removes div's that cause obstruction
    def clear_dialogs(self):

        # we want to be tracked
        # agree to any cookie requests
        self.accept_cookies()

        # TODO see if clicking main content will escape any popups

        dialogs = self.driver.find_elements_by_css_selector("[id*=dialog]")

        #TODO Can dialogs be encapsulated in classes?
        #dialogs_with_class = self.driver.find_elements_by_css_selector("[class*=dialog]")

        for dialog in dialogs:
            try:
                self.driver.execute_script("arguments[0].remove();", dialog)
                log.info('Removed a dialog')
            except:
                log.error('error in removing dialog')


    def accept_cookies(self):

        agree_buttons = self.driver.find_elements_by_xpath(
            "//button[contains(string(), 'Agree') or contains(string(), 'Allow') or contains(string(), 'Accept')] ")
        for button in agree_buttons:
            try:
                button.click()
                log.info('Clicked a button')
                sleep(randint(1, 2))
            except:
                log.error('Failed to click a button')


    def click_local_links(self, current_depth):

        local_links = self.driver.find_elements_by_xpath("//a[not(contains(href, 'http'))]")

        #favour middle half
        start_range = math.ceil(len(local_links) / 4)
        end_range = math.ceil(len(local_links) - (len(local_links) / 4))

        #try n number of times to click a random link.
        #do not try more number of times then there is elements
        for i in range(len(local_links)):
            random_pos = randint(start_range, end_range)
            if (self.isElementClickable(local_links[random_pos])):
                try:
                    #local_links[random_pos].click()
                    linkURL = local_links[random_pos].get_attribute('href')
                    self.traverse([linkURL], current_depth-1)
                    log.info('Clicked a local link')
                    break
                except:
                    log.error('Failed to click local link')

    def isElementClickable(self, element):

        # is element visible by styles
        if (not element.is_displayed()):
            return False
        return True

        #TODO check if behind anything
        #
        # # is the element behind another element
        boundingRect = element.rect
        #
        # // adjust coordinates to get more accurate results
        # const left = boundingRect.left + 1;
        # const right = boundingRect.right - 1;
        # const top = boundingRect.top + 1;
        # const bottom = boundingRect.bottom - 1;
        #
        # if (document.elementFromPoint(left, top) !== element ||
        #     document.elementFromPoint(right, top) !== element ||
        #     document.elementFromPoint(left, bottom) !== element ||
        #     document.elementFromPoint(right, bottom) !== element) {
        #     return false;
        # }
        #
        # return true;
        # `;
        #
        # return element.getDriver().executeScript(SCRIPT, element);

    def full_page_screenshot(self, url):

        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(required_width, required_height)
        # elem.screenshot('/pageScreenshot/' + url + '.png')  # avoids scrollbar

        try:

            with open('pageScreenshots/' + str(randint(0, 10000)) + '.png', 'wb+') as fh:
                fh.write(base64.b64decode(self.driver.get_screenshot_as_base64()))

            log.info('printed full page')
        except:
            log.error('Full page screenshot failed')

        self.driver.set_window_size(original_size['width'], original_size['height'])

    def random_wait_and_scroll(self):
        # random wait and scroll action
        log.info('Waiting...')
        for i in range(3):
            sleep(randint(1, 3))
            self.driver.execute_script("window.scrollTo(0," + str(randint(50, 2000)) + ")")
            sleep(randint(1, 3))

    #prevent them from getting in the way of ads
    def remove_header(self):

        headers = self.driver.find_elements_by_xpath("//div[contains(@class, 'header')] | //header[@class]")
        #//header[@class]" or
        for header in headers:
                try:
                    self.driver.execute_script("arguments[0].remove();", header)
                    log.info('removed a header')
                except:
                    log.error('error in removing header')

def timer():
    for i in range(15):
        sleep(1)

if __name__ == '__main__':

    webdriver = "chromedriver.exe"
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = Chrome(webdriver, chrome_options=chrome_options)

    bot = Bot('Mr', 'West', 'mwest5078', 'password', 'gender', 'birthDay', 'birthMonth', 'birthYear', 'politicalStance', 'search_terms', 'profileBuilt')
    trav = webTraverse(driver, bot, True)
    trav.traverse()

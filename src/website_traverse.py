from google_adsense_scrape import getGoogleAds
from bot import Bot
from database import Database
from random import random, randint
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import base64
import math


class webTraverse:
    """Methodical traversal or set of websites with scraping if required.

    Use traverse to being traversal

        Attributes:
            driver (obj: WebDriver): To traverse with. MUST be headless for full page screenshots to work
            scrape (Bool): Whether sraping is required .

        """
    def __init__(self, driver, database, bot, scrape=False):
        self.driver = driver
        self.toScrape = scrape
        self.database = database
        self.bot = bot

    def traverse(self):

        urls = open('urls.txt', 'r')

        for url in urls:
            print('Opening ' + url)
            self.driver.get(url)

            print('Waiting...')
            sleep(randint(10, 15))

            # dialogues can get in the way of ads and scrolling
            self.clear_dialogs()

            self.remove_header()

            self.random_wait_and_scroll()

            if self.toScrape:
                self.full_page_screenshot(url)
                getGoogleAds(self.driver, self.database, self.bot)

            self.click_local_links()

            self.random_wait_and_scroll()

    # removes div's that cause obstruction
    def clear_dialogs(self):

        # we want to be tracked
        # agree to any cookie requests
        self.accept_cookies()

        # TODO see if clicking main content will escape any popups

        dialogs = driver.find_elements_by_css_selector("[id*=dialog]")

        #TODO Can dialogs be encapsulated in classes?
        #dialogs_with_class = driver.find_elements_by_css_selector("[class*=dialog]")

        for dialog in dialogs:
            try:
                driver.execute_script("arguments[0].remove();", dialog)
                print('Removed a dialog')
            except:
                print('error in removing dialog')


    def accept_cookies(self):

        agree_buttons = driver.find_elements_by_xpath(
            "//button[contains(string(), 'Agree') or contains(string(), 'Allow') or contains(string(), 'Accept')] ")
        for button in agree_buttons:
            try:
                button.click()
                print('Clicked a button')
                sleep(random.random())
            except:
                print('Failed to click a button')


    def click_local_links(self):

        local_links = driver.find_elements_by_xpath("//a[not(contains(href, 'http'))]")

        #favour middle half
        start_range = math.ceil(len(local_links) / 4)
        end_range = math.ceil(len(local_links) - (len(local_links) / 4))

        #try n number of times to click a random link.
        #do not try more number of times then there is elements
        for i in range(len(local_links)):
            random_pos = randint(start_range, end_range)
            if (self.isElementClickable(local_links[random_pos])):
                try:
                    print(local_links[random_pos].location_once_scrolled_into_view)
                    local_links[random_pos].click()
                    print('Clicked a local link')
                    break
                except:
                    print('Failed to click local link')

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

        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        # elem.screenshot('/pageScreenshot/' + url + '.png')  # avoids scrollbar

        try:

            with open('pageScreenshots/' + str(randint(0, 10000)) + '.png', 'wb+') as fh:
                fh.write(base64.b64decode(driver.get_screenshot_as_base64()))

            print('printed full page')
        except:
            print('Full page screenshot failed')

        driver.set_window_size(original_size['width'], original_size['height'])

    def random_wait_and_scroll(self):
        # random wait and scroll action
        print('Waiting...')
        for i in range(3):
            sleep(randint(1, 3))
            driver.execute_script("window.scrollTo(0," + str(randint(50, 2000)) + ")")
            sleep(randint(1, 3))

    #prevent them from getting in the way of ads
    def remove_header(self):

        headers = driver.find_elements_by_xpath("//div[contains(@class, 'header')] | //header[@class]")
        #//header[@class]" or
        for header in headers:
                try:
                    driver.execute_script("arguments[0].remove();", header)
                    print('removed a header')
                except:
                    print('error in removing header')


if __name__ == '__main__':

    webdriver = "chromedriver.exe"
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = Chrome(webdriver, chrome_options=chrome_options)

    db = Database()
    trav = webTraverse(driver, db, None, True)
    trav.traverse()






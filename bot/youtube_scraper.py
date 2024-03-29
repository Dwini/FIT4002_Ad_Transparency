import os
from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from enum import Enum
import requests
from youtube_elements import youtube_elements
from PIL import Image
import io
import math
import base64
import logging

log = logging.getLogger()

class yt_ad(Enum):
    ALL = 1
    VIDEO = 2
    SIDEBAR = 3


class youtube_scraper:
    def __init__(self, webdriver, bot, adType=yt_ad.ALL):
        """
        :param webdriver: the driver for the selenium project
        :param adType: enable saving of different adTypes, defaults to ALL. Use enum to switch between ALL, VIDEO, SIDEBAR, PROMO_VIDEO. Used for debugging.
        """
        self.webdriver = webdriver
        self.bot = bot

        self.enableVideoAds = False
        self.enableSidebarAds = False

        self.check_ad_type(adType)

        # Get Keywords
        self.keywords = bot.getSearchTerms()

        self.yt_element_search = youtube_elements(webdriver)

    def scrape_youtube_video_ads(self, search_param=None, timeout=10):
        """
        :param search_param: string - search parameters for the youtube video that you want to find
        :param timeout: time in seconds that you want to keep checking the page for a ad
        :return: returns true if ad is found, otherwise returns False.
        """
        wait = WebDriverWait(self.webdriver, 5)
        if search_param is not None:
            self.search_video(search_param)
        else:
            self.webdriver.get('https://www.youtube.com/')
            self.webdriver.find_element_by_id(
                'video-title').click()  # click first result

        # wait until the title of the video is loaded onto the page
        v_title = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
        self.log_to_db(self.bot.getUsername(), self.webdriver.current_url, 'visit')

        foundVideoAd = False
        foundSidebarAd = False

        attempt = 0
        sleep(10)  # hard coded sleep to bypass some ad load times.

        # save baseline screenshot of current page usually for debugging
        try:
            self.webdriver.save_screenshot('current_webpage.png')
        except Exception as e:
            log.error(str(e))

        while (attempt < timeout) or not (foundVideoAd and foundSidebarAd):
            sleep(1)
            attempt += 1

            if self.enableVideoAds and not foundVideoAd:
                try:
                    video_ad = self.yt_element_search.find_video_ad()
                    foundVideoAd = True

                    video_ad_url = self.yt_element_search.find_video_ad_url(video_ad)
                    video_element = self.webdriver.find_element_by_class_name('html5-video-player')

                    log.info('Attempt ' + str(attempt) + ' Screenshotting video/panel advertisement')
                    self.screenshot_ad(video_element, False, 'video_ad.png', True)

                    # find the video id for the advertisment
                    log.info('Finding video ad id')
                    ad_id = self.get_ad_id()
                    if ad_id is not None:
                        # todo: db call inclusive with ad_id.
                        log.info('ad video id: ' + str(ad_id))
                        self.save_ad(self.bot.getUsername(), video_ad_url, video_ad_url, video_ad, 'video_ad.png')
                    else:
                        # normal db call
                        self.save_ad(self.bot.getUsername(), video_ad_url, video_ad_url, video_ad, 'video_ad.png')
                    log.info('Attempt ' + str(attempt) + ' SAVED - video/panel advertisement')

                except NoSuchElementException:
                    pass

            if self.enableSidebarAds and not foundSidebarAd:
                try:
                    sidebar_ad = self.yt_element_search.find_sidebar_ad()

                    # as the elements for sidebar ads can exist on the page, but are 0x0 check for this.
                    dimensions = sidebar_ad.size
                    if (dimensions['width'] == 0 or dimensions['height'] == 0):
                        return NoSuchElementException

                    foundSidebarAd = True
                    sidebar_ad_url = self.yt_element_search.find_sidebar_ad_url(sidebar_ad.get_attribute('innerHTML'))

                    coordinates = sidebar_ad.location_once_scrolled_into_view
                    # self.webdriver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

                    # this will only take a proper screenshot, when running in a larger window or headlessly
                    self.screenshot_ad(sidebar_ad, False, 'sidebar_ad.png', True)

                    self.save_ad(self.bot.getUsername(), sidebar_ad_url, sidebar_ad_url, sidebar_ad.get_attribute('innerHTML'), 'sidebar_ad.png')
                    log.info('Attempt ' + str(attempt) + ' SAVED - sidebar advertisement')
                    break
                except NoSuchElementException:
                    pass

        log.info('finalizing youtube search for: ' + str(search_param))

        if (foundSidebarAd or foundVideoAd) is False:
            log.warning('No ads found')

        sleep(1)

        return foundSidebarAd or foundVideoAd

### HELPER FUNCTIONS ###
    def change_bot(self, bot):
        # helper function so that we dont need to re instantiate the class if we want to use a different bot to scrape
        self.bot = bot

    def check_ad_type(self, adType):

        if adType == yt_ad.ALL:
            self.enableVideoAds = True
            self.enableSidebarAds = True
        elif adType == yt_ad.VIDEO:
            self.enableVideoAds = True
        elif adType == yt_ad.SIDEBAR:
            self.enableSidebarAds = True

    def search_video(self, search_param):
        self.webdriver.get(
            'https://www.youtube.com/results?search_query=' + str(search_param))
        self.log_to_db(self.bot.getUsername(), 'https://www.youtube.com/results?search_query=' + str(search_param), 'search', str(search_param))
        sleep(3)

        try:
            promo_video_ads = self.yt_element_search.find_promo_search_video_ad()
            if promo_video_ads is not None:
                for ad in promo_video_ads[:-1]:
                    log.info('Found - promoted video advertisement')
                    promo_video_ad_url = self.yt_element_search.find_promo_search_video_ad_url(ad.get_attribute('innerHTML'))

                    self.screenshot_ad(ad, False, 'promo_video_ad.png', True)

                    self.save_ad(self.bot.getUsername(), promo_video_ad_url, promo_video_ad_url, ad.get_attribute('innerHTML'), 'promo_video_ad.png')

        except NoSuchElementException:
            log.warning('No promo vid ads found')
            pass

        self.webdriver.find_element_by_id('video-title').click()  # click first result

    def get_video_length(self):
        """
        :return: returns an int for the amount of seconds in the youtube video
        """
        wait = WebDriverWait(self.webdriver, 10)
        # todo: also frequently does not get the timestamp if lower sleep/webdriverwait

        try:
            duration = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ytp-time-duration')))
            sleep(5)
            date_time = get_sec(duration.text)
            return date_time
        except ValueError:
            raise NoSuchElementException('Could not find time on Webpage')

    def save_ad(self, bot, ad_link, ad_headline, ad_html, image=None):
        # save ad to database with attached image
        data = {
            "bot": bot,
            "link": ad_link,
            "headline": ad_headline,
            "html": ad_html,
        }
        log.info('saving ad... ' + str(data['headline']))
        file = {'file': open(image, 'rb')}
        url = os.getenv('DB_URL') + '/ads'
        r = requests.post(url, files=file, data=data)
        r.raise_for_status()

    def log_to_db(self, bot_id, url, action, search_term=None):
        # Logs table deprecated. Just need to send to log
        if search_term is not None:
            log.info('Searching for "' + search_term + '" at ' + url)
        else:
            log.info(action + ' at ' + url)

    def screenshot_ad(self, html_element, base64=True, name="current_Ad.png", crop=False):
        if crop:
            location = html_element.location
            size = html_element.size
            # debug to catch any NS_ERROR_LOSS_OF_SIGNIFICANT_DATA errors
            # if image is too big.
            try:
                self.webdriver.save_screenshot(name)
            except Exception as e:
                log.error(str(e))
                log.error('window size: '+str(self.webdriver.get_window_size()))
                log.error('image size: '+str(size))
                log.error('location: '+str(location))

            # crop image
            x = location['x']
            y = location['y']
            width = location['x']+size['width']
            height = location['y']+size['height']
            im = Image.open(name)
            im = im.crop((int(x), int(y), int(width), int(height)))
            im.save(name)

        else:
            try:
                if base64:
                    screenshot = html_element.screenshot_as_base64
                else:
                    # debug to catch any NS_ERROR_LOSS_OF_SIGNIFICANT_DATA errors
                    # if image is too big.
                    try:
                        self.webdriver.save_screenshot(name)
                    except Exception as e:
                        log.error(str(e))
                        log.error('window size: '+str(self.webdriver.get_window_size()))
                        log.error('image size: '+str(size))
            except:
                log.warning('Screenshot capture failed')

    def get_sec(self, time_string):
        """
        :param time_string: string in the form HH:MM:SS
        :return: returns int converted from string to time in seconds
        """

        if len(time_string.split(':')) == 2:
            m, s = time_string.split(':')
            return int(m) * 60 + int(s)

        elif len(time_string.split(':')) == 3:
            h, m, s = time_string.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)

    def get_ad_id(self):
        try:
            # right click on the video player
            player = self.webdriver.find_element_by_class_name('html5-video-player')
            actionChains = ActionChains(self.webdriver)
            actionChains.context_click(player).perform()

            # open stats for nerds
            self.webdriver.find_element_by_xpath("//div[@class='ytp-menuitem'][6]/div[@class='ytp-menuitem-label'][1]").click()
            sleep(1)
            value = self.webdriver.find_element_by_xpath("//*[@id='movie_player']/div[18]/div/div[1]/span").text
            ad_id = value[0:11]
            return ad_id
        except NoSuchElementException:
            log.warn('Unable to find video ad ID')
            pass
        return None

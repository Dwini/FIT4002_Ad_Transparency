from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum

class yt_ad(Enum):
    ALL = 1
    VIDEO = 2
    SIDEBAR = 3
    PROMO_VIDEO = 4

class youtube_scraper:
    def __init__(self, webdriver, db, adType):
        """
        :param webdriver: the driver for the selenium project
        :param videoAds: enable saving of youtube video Ads, defaults to false
        :param sidebarAds: enable saving of youtube sidebar Ads, defaults to false
        :param videoAds: enable saving of youtube video Ads, defaults to false
        """
        self.webdriver = webdriver
        self.db = db
        self.ads = []  # can be refactored into dictionary, as right now only contains the html element

        self.enableVideoAds = False
        self.enableSidebarAds = False
        self.enablePromoVideoAds = False

        if adType == yt_ad.ALL:
            self.enableVideoAds = True
            self.enableSidebarAds = True
            self.enablePromoVideoAds = True
        elif adType == yt_ad.VIDEO:
            self.enableVideoAds = True
        elif adType == yt_ad.SIDEBAR:
            self.enableSidebarAds = True
        elif adType == yt_ad.PROMO_VIDEO:
            self.enablePromoVideoAds = True

    def search_video(self, search_param):
        self.webdriver.get('https://www.youtube.com/results?search_query=' + str(search_param))
        sleep(3)
        self.webdriver.find_element_by_id('video-title').click()  # click first result

    def scrape_youtube_video_ads(self, search_param = None, timeout = 10):
        """
        :param search_param: search parameters for the youtube video that you want to find
        :param watch: if you want to set the bot to actually stay on the youtube video for longer
        :param timeout: time in seconds that you want to keep checking the page for a ad
        :return: returns true if ad is found, otherwise returns False.
        # todo: db queries can be put in here or webscraper class.
        """
        wait = WebDriverWait(self.webdriver, 5)
        if search_param is not None:
            self.search_video(search_param)
        else:
            self.webdriver.get('https://www.youtube.com/')
            self.webdriver.find_element_by_id('video-title').click()  # click first result

        v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
        # todo: probably save the video title that we're watching somewhere

        foundVideoAd = False
        foundSidebarAd = False
        foundPromoVideoAd = False

        attempt = 0
        sleep(3)
        self.webdriver.save_screenshot('base_Attempt.png')

        while (attempt < timeout) or (foundPromoVideoAd and foundSidebarAd and foundVideoAd):
            sleep(1)
            # ideally all of these print statements should be redirected to out to a log file
            attempt += 1

            if self.enableVideoAds and not foundVideoAd:
                try:
                    panel_ad = self.find_panel_ad(self.webdriver)
                    self.ads.append(panel_ad)
                    foundVideoAd = True
                    print('Attempt ' + str(attempt) + ' Found - video/panel advertisement')
                except NoSuchElementException:
                    pass

            if self.enableSidebarAds and not foundSidebarAd:
                try:
                    sidebar_ad = self.find_sidebar_ad(self.webdriver)

                    self.ads.append(sidebar_ad)
                    foundSidebarAd = True
                    print('Attempt ' + str(attempt) + ' Found - sidebar advertisement')
                except NoSuchElementException:
                    pass

            if self.enablePromoVideoAds and not foundPromoVideoAd:
                try:
                    promo_video_ad = self.find_promo_video_ad(self.webdriver)
                    self.ads.append(promo_video_ad)
                    foundPromoVideoAd = True
                    print('Attempt ' + str(attempt) + ' Found - promoted video advertisement')
                except NoSuchElementException:
                    pass

        if (foundPromoVideoAd or foundSidebarAd or foundVideoAd) is False:
            print('No ads found')

        return foundPromoVideoAd or foundSidebarAd or foundVideoAd

    def find_panel_ad(self, webdriver):
        # todo: this is flaky, and will often miss video advertisements,
        try:
            panel_ad = webdriver.find_element_by_class_name("ytp-flyout-cta-headline")
        except NoSuchElementException:
            try:
                panel_ad = webdriver.find_element_by_css_selector(".ytp-ad-button.ytp-ad-visit-advertiser-button.ytp-ad-button-link")
            except NoSuchElementException:
                try:
                    panel_ad = webdriver.find_element_by_css_selector(".ytp-ad-button-text")
                except NoSuchElementException:
                    raise NoSuchElementException('No video ad found')
        return panel_ad.get_attribute('outerHTML')

    def find_promo_video_ad(self, webdriver):
        promo_video_ad = webdriver.find_element_by_class_name(
            'style-scope ytd-compact-promoted-video-renderer')
        return promo_video_ad.get_attribute('outerHTML')

    def find_sidebar_ad(self, webdriver):
        try:
            sidebar_ad_title = webdriver.find_element_by_class_name('style-scope ytd-action-companion-ad-renderer')
        except NoSuchElementException:
            try:
                sidebar_ad_title = webdriver.find_element_by_class_name(
                    'style-scope ytd-promoted-sparkles-web-renderer')
            except NoSuchElementException:
                raise NoSuchElementException('No sidebar ad found')
        return sidebar_ad_title.get_attribute('outerHTML')

    def get_video_length(self):
        """
        :return: returns an int for the amount of seconds in the youtube video
        """
        wait = WebDriverWait(self.webdriver, 10)
        # todo also frequently does not get the timestamp if lower sleep/webdriverwait

        try:
            duration = wait.until(EC.presence_of_element_located(
                           (By.CLASS_NAME, 'ytp-time-duration')))
            sleep(5)
            date_time = get_sec(duration.text)
            return date_time
        except ValueError:
            raise NoSuchElementException('Could not find time on Webpage')

def get_sec(time_string):
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


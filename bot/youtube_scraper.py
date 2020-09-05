import os
from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum
from lxml import html
import requests

DB_URL = os.getenv('DB_URL') or "http://localhost:8080"


class yt_ad(Enum):
    ALL = 1
    VIDEO = 2
    SIDEBAR = 3
    PROMO_VIDEO = 4


class youtube_scraper:
    def __init__(self, webdriver, bot, adType=yt_ad.ALL):
        """
        :param webdriver: the driver for the selenium project
        :param adType: enable saving of different adTypes, defaults to ALL. Use enum to switch between ALL, VIDEO, SIDEBAR, PROMO_VIDEO. Used for debugging.
        """
        self.webdriver = webdriver
        self.ads = []  # can be refactored into dictionary, as right now only contains the html element
        self.bot = bot

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

        # Get Keywords
        self.keywords = bot.getSearchTerms()

    def search_video(self, search_param):
        self.webdriver.get(
            'https://www.youtube.com/results?search_query=' + str(search_param))
        # self.log_search_to_db(self.bot.getUsername(), 'https://www.youtube.com/results?search_query=' + str(search_param), str(search_param))
        sleep(3)
        self.webdriver.find_element_by_id(
            'video-title').click()  # click first result

    def scrape_youtube_video_ads(self, search_param=None, timeout=10, repeat=False):
        """
        :param search_param: search parameters for the youtube video that you want to find
        :param watch: if you want to set the bot to actually stay on the youtube video for longer
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

        v_title = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
        # todo: probably save the video title that we're watching somewhere

        foundVideoAd = False
        foundSidebarAd = False
        foundPromoVideoAd = False

        attempt = 0
        sleep(5)
        self.webdriver.save_screenshot('current_webpage.png')

        while (attempt < timeout) or (foundVideoAd and foundSidebarAd and foundPromoVideoAd):
            sleep(2)
            # ideally all of these print statements should be redirected to out to a log file
            attempt += 1

            if self.enableVideoAds and not foundVideoAd:
                try:
                    panel_ad = self.find_video_ad(self.webdriver)
                    foundVideoAd = True

                    video_ad_name = self.find_video_ad_name(panel_ad)
                    video_ad_url = self.find_video_ad_url(panel_ad)

                    save_ad(self.bot.getUsername(), video_ad_url, video_ad_url, panel_ad)
                    print('Attempt ' + str(attempt) +
                          ' Found - video/panel advertisement')
                except NoSuchElementException:
                    pass

            if self.enableSidebarAds and not foundSidebarAd:
                try:
                    sidebar_ad = self.find_sidebar_ad(self.webdriver)
                    foundSidebarAd = True

                    sidebar_ad_name = self.find_sidebar_ad_name(sidebar_ad)
                    sidebar_ad_url = self.find_sidebar_ad_url(sidebar_ad)

                    save_ad(self.bot.getUsername(), sidebar_ad_url, sidebar_ad_name, sidebar_ad)

                    sidebar_ad = self.find_secondary_sidebar_ad(self.webdriver)
                    print(sidebar_ad)
                    foundSidebarAd = True

                    sidebar_ad_name = self.find_secondary_sidebar_ad_name(sidebar_ad)
                    sidebar_ad_url = self.find_secondary_sidebar_ad_url(sidebar_ad)

                    save_ad(self.bot.getUsername(), sidebar_ad_url, sidebar_ad_name, sidebar_ad)
                    print('Attempt ' + str(attempt) +
                          ' Found - sidebar advertisement')
                except NoSuchElementException:
                    pass

            if self.enablePromoVideoAds and not foundPromoVideoAd:
                try:
                    promo_video_ad = self.find_promo_video_ad(self.webdriver)
                    foundPromoVideoAd = True
                    save_ad(self.bot.getUsername(), 'promo vid url', 'promo vid ad', promo_video_ad)
                    print('Attempt ' + str(attempt) +
                          ' Found - promoted video advertisement')
                except NoSuchElementException:
                    pass

        if (foundPromoVideoAd or foundSidebarAd or foundVideoAd) is False:
            print('No ads found')

        return foundPromoVideoAd or foundSidebarAd or foundVideoAd

    def find_video_ad(self, webdriver):
        # todo: this is flaky, and will sometimes miss video advertisements, if no banner is set on the ad
        try:
            # this can find ads for ads like ubereats and grammarly, that have a banner on the left.
            panel_ad = webdriver.find_element_by_class_name(
                "ytp-flyout-cta-body")
        except:
            try:
                panel_ad = webdriver.find_element_by_class_name(
                    "ytp-flyout-cta-headline-container")
            except NoSuchElementException:
                try:
                    panel_ad = webdriver.find_element_by_css_selector(
                        ".ytp-ad-button.ytp-ad-visit-advertiser-button.ytp-ad-button-link")
                except NoSuchElementException:
                    try:
                        panel_ad = webdriver.find_element_by_css_selector(
                            ".ytp-ad-button-text")
                    except NoSuchElementException:
                        raise NoSuchElementException('No video ad found')
        return panel_ad.get_attribute('outerHTML')

    def find_promo_video_ad(self, webdriver):
        promo_video_ad = webdriver.find_element_by_class_name(
            'style-scope ytd-compact-promoted-video-renderer')
        return promo_video_ad.get_attribute('outerHTML')

    def find_sidebar_ad(self, webdriver):
        try:
            sidebar_ad_title = webdriver.find_element_by_class_name(
                'yt-simple-endpoint style-scope ytd-action-companion-ad-renderer')
            self.screenshot_ad(sidebar_ad_title)
        except NoSuchElementException:
            try:
                sidebar_ad_title = webdriver.find_element_by_class_name(
                    'style-scope ytd-action-companion-ad-renderer')
            except NoSuchElementException:
                raise NoSuchElementException('No sidebar ad found')

        return sidebar_ad_title.get_attribute('outerHTML')

    def find_secondary_sidebar_ad(self, webdriver):
        try:
            sidebar_ad_title = webdriver.find_element_by_class_name(
                'style-scope ytd-promoted-sparkles-web-renderer')
            self.screenshot_ad(sidebar_ad_title)

        except NoSuchElementException:
            raise NoSuchElementException('No secondary sidebar ad found')

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

    def save_ad(self, bot, ad_link, ad_headline, ad_html):
        # save ad to database
        r = requests.post(DB_URL+'/ads', data={
            "bot": bot,
            "link": ad_link,
            "headline": ad_headline,
            "html": ad_html
        })
        r.raise_for_status()

    def log_search_to_db(self, bot_id, url, search_term):
        # save site visit to database
        r = requests.post(DB_URL+'/logs', data={
            "bot": bot_id,
            "url": url,
            "actions": ['search'],
            "search_term": search_term
        })
        r.raise_for_status()

    def find_video_ad_name(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            video_ad_name = ad_html.xpath(
                '//div[@class="ytp-ad-text ytp-flyout-cta-headline"]')[0].text
        except Exception:
            print('HTML parse - Unable to find ad name, setting default name')
            video_ad_name = 'video_ad_name'
        return video_ad_name

    def find_video_ad_url(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            video_ad_url = ad_html.xpath(
                '//div[@class="ytp-ad-text ytp-flyout-cta-description"]')[0].text
        except Exception:
            print('HTML parse - Unable to find ad url, setting default name')
            video_ad_url = 'video_ad_url'
        return video_ad_url

    def find_sidebar_ad_name(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            sidebar_ad_name = ad_html.xpath('//div[@id = "header"]')[0].text
        except Exception:
            print('HTML parse - Unable to find ad name, setting default name')
            sidebar_ad_name = 'sidebar_ad_name'
        return sidebar_ad_name

    def find_sidebar_ad_url(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            sidebar_ad_url = ad_html.xpath('//span[@id = "domain"]')[0].text
        except Exception:
            print('HTML parse - Unable to find ad url, setting default name')
            sidebar_ad_url = 'sidebar_ad_url'
        return sidebar_ad_url

    def screenshot_ad(self, html_element, base64=True):
        try:
            html_element.location_once_scrolled_into_view
            try:
                if base64:
                    screenshot = html_element.screenshot_as_base64
                # print(base64_screenshot)
                # might include the db call, or in actual save ad function
                else:
                    screenshot = html_element.save_screenshot("current_Ad.png")
            except:
                print('Screenshot capture failed')
        except Exception:
            pass

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

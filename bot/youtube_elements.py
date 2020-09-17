from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import logging

LOGGER = logging.getLogger()

class youtube_elements:

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def find_video_ad(self):
        # this function finds in-stream video ads based on HTMl elements.
        try:
            # try to find ad:
            video_ad = self.webdriver.find_element_by_xpath("//*[starts-with(@id, 'visit-advertiser:')]")
        except NoSuchElementException:
            try:
                video_ad = self.webdriver.find_element_by_class_name("ytp-flyout-cta-body")
            except NoSuchElementException:
                raise NoSuchElementException('Unable to locate Video ad - No video ad found')
            ### CLEANUP: Marking the rest of these irrelevant for now. ###
                # try:
                #     panel_ad = self.webdriver.find_element_by_class_name(
                #         "ytp-flyout-cta-headline-container")
                # except NoSuchElementException:
                #     try:
                #         panel_ad = self.webdriver.find_element_by_css_selector(
                #             ".ytp-ad-button.ytp-ad-visit-advertiser-button.ytp-ad-button-link")
                #     except NoSuchElementException:
                #         try:
                #             panel_ad = self.webdriver.find_element_by_css_selector(
                #                 ".ytp-ad-button-text")
                #         except NoSuchElementException:
                #             raise NoSuchElementException('No video ad found')
        return video_ad.get_attribute('outerHTML')

    def find_video_ad_url(self, html_string):
        """
        this currently attempts to try parse the html for the current lines of code:
        
        self.webdriver.find_element_by_xpath("//*[starts-with(@id, 'visit-advertiser:')]")
        
        self.webdriver.find_element_by_class_name("ytp-flyout-cta-body")
        """
        try:
            ad_html = html.fromstring(html_string)
            video_ad_url = ad_html.xpath('//span[@class="ytp-ad-button-text"][1]')[0].text
        except Exception:
            try:
                video_ad_url = ad_html.xpath('//div[@class="ytp-ad-text ytp-flyout-cta-description"]')[0].text
            except Exception:
                LOGGER.warning('HTML parse - Unable to find ad url, setting default name')
                video_ad_url = 'video_ad_url'
        return video_ad_url

    def find_promo_search_video_ad(self):
        """
        this function should be called during a youtube search result, to check for promoted videos.
        """
        try:
            ads = self.webdriver.find_elements_by_xpath('//*[@id="contents"]/ytd-item-section-renderer')
            #self.webdriver.save_screenshot('during_search.png')
            return ads
            
        except NoSuchElementException:
            raise NoSuchElementException('Unable to locate promo vid ads - No promo ads found')
            pass
            return None

    def find_promo_search_video_ad_url(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            promo_search_video_ad_url = ad_html.xpath('//span[@class="style-scope yt-formatted-string"][1]')[0].text
        except Exception:
            LOGGER.warning('HTML parse - Unable to find ad url, setting default name')
            promo_search_video_ad_url = 'promo_search_video_ad_url'
        return promo_search_video_ad_url

    def find_sidebar_ad(self):
        try:
            sidebar_ad = self.webdriver.find_element_by_id('player-ads')
            # self.screenshot_ad(sidebar_ad)
        except NoSuchElementException:
            raise NoSuchElementException('No sidebar ad found')

        return sidebar_ad
    
    def find_sidebar_ad_url(self, html_string):
        try:
            ad_html = html.fromstring(html_string)
            sidebar_ad_url = ad_html.xpath('//span[@id="domain"]')[0].text
        except Exception:
            LOGGER.warning('HTML parse - Unable to find sidebar_ad url, setting default name')
            sidebar_ad_url = 'sidebar_ad_url'
        return sidebar_ad_url

    # def find_masthead_ad(self):
    # # this will only need to run when we load the youtube home page.
    #     try:
    #         masthead_ad = webdriver.find_element_by_class_name('masthead_ad')
    #         self.screenshot_ad(masthead_ad)

    #     except NoSuchElementException:
    #         raise NoSuchElementException('No masthead ad found')

    #     return masthead_ad.get_attribute('outerHTML')
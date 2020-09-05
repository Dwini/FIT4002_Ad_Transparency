from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import html


class youtube_elements:

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def find_video_ad(self):
        # this function finds in-stream video ads based on HTMl elements.
        # todo: this is flaky, and will sometimes miss video advertisements
        try:
            # try to find ad:
            panel_ad = self.webdriver.find_element_by_xpath("//*[starts-with(@id, 'visit-advertiser:')]")
        except NoSuchElementException:
            try:
                panel_ad = self.webdriver.find_element_by_class_name("ytp-flyout-cta-body")
            except NoSuchElementException:
                raise NoSuchElementException('Unable to locate Video ad - No video ad found')
            ### Marking the rest of these irrelevant for now. ###
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
        return panel_ad.get_attribute('outerHTML')

    def find_promo_search_video_ad(self):
        try:
            ads = webdriver.find_element_by_class_name('ytd-promoted-sparkles-text-search-renderer')
            print(ads[0])
        except NoSuchElementException:
                raise NoSuchElementException('Unable to locate promo vid ads - No promo ads found')


    # def find_promo_video_ad(self):
    #     promo_video_ad = webdriver.find_element_by_class_name(
    #         'style-scope ytd-compact-promoted-video-renderer')
    #     return promo_video_ad.get_attribute('outerHTML')

    # def find_sidebar_ad(self):
    #     try:
    #         sidebar_ad_title = webdriver.find_element_by_class_name(
    #             'yt-simple-endpoint style-scope ytd-action-companion-ad-renderer')
    #         self.screenshot_ad(sidebar_ad_title)
    #     except NoSuchElementException:
    #         try:
    #             sidebar_ad_title = webdriver.find_element_by_class_name(
    #                 'style-scope ytd-action-companion-ad-renderer')
    #         except NoSuchElementException:
    #             raise NoSuchElementException('No sidebar ad found')

    #     return sidebar_ad_title.get_attribute('outerHTML')

    # def find_secondary_sidebar_ad(self):
    #     try:
    #         sidebar_ad_title = webdriver.find_element_by_class_name(
    #             'style-scope ytd-promoted-sparkles-web-renderer')
    #         self.screenshot_ad(sidebar_ad_title)

    #     except NoSuchElementException:
    #         raise NoSuchElementException('No secondary sidebar ad found')

    #     return sidebar_ad_title.get_attribute('outerHTML')

    # def find_masthead_ad(self):
    #     try:
    #         masthead_ad = webdriver.find_element_by_class_name('masthead_ad')
    #         self.screenshot_ad(masthead_ad)

    #     except NoSuchElementException:
    #         raise NoSuchElementException('No masthead ad found')

    #     return masthead_ad.get_attribute('outerHTML')

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
                print('HTML parse - Unable to find ad url, setting default name')
                video_ad_url = 'video_ad_url'
        return video_ad_url

    # def find_sidebar_ad_name(self, html_string):
    #     try:
    #         ad_html = html.fromstring(html_string)
    #         sidebar_ad_name = ad_html.xpath('//div[@id = "header"]')[0].text
    #     except Exception:
    #         print('HTML parse - Unable to find ad name, setting default name')
    #         sidebar_ad_name = 'sidebar_ad_name'
    #     return sidebar_ad_name

    # def find_sidebar_ad_url(self, html_string):
    #     try:
    #         ad_html = html.fromstring(html_string)
    #         sidebar_ad_url = ad_html.xpath('//span[@id = "domain"]')[0].text
    #     except Exception:
    #         print('HTML parse - Unable to find ad url, setting default name')
    #         sidebar_ad_url = 'sidebar_ad_url'
    #     return sidebar_ad_url

    # def screenshot_ad(self, html_element):
    #     element = 'html5-video-player'

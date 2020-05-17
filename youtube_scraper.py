from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
import signal
import datetime

def signal_handler(signum, frame):
    raise TimeoutException("Signal handler calls timeout")

def get_video_length(webdriver):
    """
    :param webdriver:
    :return: returns an int for the amount of seconds in the youtube video
    """
    sleep(4)

    # todo need to add a check to extend the %M:%S to %H:%M:%S for longer youtube videos
    # todo also frequently does not get the timestamp even if on the page? maybe set higher sleep/webdriverwait
    try:
        duration = webdriver.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0]
        date_time = datetime.datetime.strptime(duration.text, "%M:%S")
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        return a_timedelta.total_seconds()
    except ValueError:
        raise NoSuchElementException('Could not find time on Webpage')

def scrape_youtube_video_ads(bot, webdriver, url = 'https://www.youtube.com/watch?v=PFNdIup9kS0'):
    delay = 5
    ads = []
    webdriver.get(url)
    WebDriverWait(webdriver, delay)

    panel_ad_title = None
    sidebar_ad_title = None
    promo_video_ad_title = None

    # tried implementing a timeout method, but only works on unix based machines
    # video_length = get_video_length(webdriver)

    # signal.signal(signal.SIGALRM, signal_handler) #  SIGALRM WILL ONLY WORK IN UNIX
    # signal.alarm(video_length/2)  # start alarm for half the length of the video

    # todo: parse in what gets searched in via parameters, as promoted video ads are a lot more common, we can choose to ignore them
    while panel_ad_title is None and sidebar_ad_title is None and promo_video_ad_title is None:
        sleep(2)
        # ideally all of these print statements should be redirected to out to a log file
        try:
            #todo: this is flaky, and will often miss video advertisements
            print('Attempt searching for video ad: ')
            panel_ad_title = webdriver.find_element_by_class_name("ytp-flyout-cta-headline")
            print(' - Found sidebar advertisement')
            ads.append(panel_ad_title.get_attribute('outerHTML'))
        except NoSuchElementException:
            print(' - No video/banner advertisement')
            pass

        try:
            print('Attempt searching for sidebar ad: ')
            sidebar_ad_title = webdriver.find_element_by_class_name('style-scope ytd-action-companion-ad-renderer')
            print(' - Found sidebar advertisement')
            ads.append(sidebar_ad_title.get_attribute('outerHTML'))
        except NoSuchElementException:
            print(' - No sidebar advertisement')
            pass

        try:
            print('Attempt searching for promoted video ad: ')
            promo_video_ad_title = webdriver.find_element_by_class_name('style-scope ytd-compact-promoted-video-renderer')
            print(' - Found promoted video advertisement')
            ads.append(promo_video_ad_title.get_attribute('outerHTML'))
        except NoSuchElementException:
            print(' - No promoted video advertisement')
            pass

    # signal.alarm(0)  # disable alarm

    print('youtube advertisment found')
    return ads

def yt_get_video_ad(bot, webdriver):

    try:
        ad_title = webdriver.find_element_by_class_name('ytp-flyout-cta-headline').get_attribute('outerHTML').getText()

        # we need to determine if there is either a banner ad or video ad
        try:
            # check for banner in video:
            ad_description = webdriver.find_element_by_class_name('ytp-flyout-cta-description').get_attribute('outerHTML').getText()
            return (ad_title, ad_description)

        except NoSuchElementException:
            # try and fetch video ad:
            # ytp-ad-visit-advertiser-button or ytp-ad-button-link
            ad_details = webdriver.find_element_by_class_name('ytp-ad-button-text').get_attribute('outerHTML').getText()
            return (ad_title, ad_details)

    except NoSuchElementException:
        print('No advertisement found')

def yt_get_sidebar_ad(bot, webdriver, list):
    try:
        ad_title = webdriver.find_element_by_class_name('ytd-action-companion-ad-renderer').get_attribute('outerHTML').getText()
        return ad_title
    except NoSuchElementException:
        print('No advertisement found')

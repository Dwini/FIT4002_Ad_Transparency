# import external libraries.
import os
import re
from random import seed, randint
import requests
import base64
import io
import math
from PIL import Image
import logging

# import local modules.
import webscraper

log = logging.getLogger()

#given a selenium driver retrieves a list of google ads which appear on the page
def getGoogleAds(driver, bot):
    seed(231)

    # google ads appear in iframes labelled as such
    iframes = driver.find_elements_by_xpath("//iframe[@data-google-container-id]")

    # Writing to a file
    #adLinks = open('../../adLinks.txt', 'w')


    screenshots = []

    for iframe in iframes:

        try:
            iframe.location_once_scrolled_into_view
        except:
            log.warning('Element location not found or not visible')

        switch_to_frame_context(driver, iframe)

        adLink = find_ad_redirect(driver)

        # if adlink is None, set to arbitrary string.
        adLink = adLink if adLink is not None else '-'

        driver.switch_to.default_content()
        base64_screenshot = ""
        try:
            #base64_screenshot = iframe.screenshot_as_base64
            png = iframe.screenshot_as_png
            image = imageProcessing(png)
        except:
            log.error('Screenshot capture failed')
            image = None

        # attempt to get the current url.
        try: current_url = self.webdriver.current_url
        except: current_url = None

        try:
            log.info('attempting to upload ad to db: '+adLink)
            url = os.getenv('DB_URL') + '/ads'
            r = requests.post(url, files={'file': image}, data={
                "bot": bot.username,
                "link": adLink,
                "headline": adLink,
                "logged_in": webscraper.successful_login,
                "current_page": current_url,
                "html": "innerHTML"
            })
            r.raise_for_status()

        # except requests.exceptions.HTTPError as e:
        #     print('Screenshot saving failed')
        #     print(e.response.text)

        #testing purposes:
        except Exception as e:
            log.error(str(e))
            log.error("Connection for Screenshot failed")


    return screenshots


def find_ad_redirect(driver):


    try:
        #adElem = driver.find_element_by_id(iframeID)

        # find the link embedded in the iframe
        linkElements = driver.find_elements_by_xpath(".//a[@href]")
    except:
        log.error('Cannot find internal link, check correct context is set')
        return None

    adLink = None
    # find the ad-redirect link with the required payload
    for linkElement in linkElements:
        adLink = extractEmbeddedUrl(linkElement.get_attribute('href'))
        if adLink is not None:
            break

        # adLinks.write(
        #    (extractEmbeddedUrl(
        #        linkElement.get_attribute('href'))
        #    )
        # )

    return adLink


def get_ad_html(driver):
    innerHTML = None
    # Get ad html
    try:
        # innerHTML = driver.find_element_by_xpath(".//html[@*]").get_attribute('innerHTML')
        #adElem = driver.find_element_by_id(iframeID)
        innerHTML = driver.find_element_by_xpath(".//html[@*]").get_attribute('innerHTML')
    except:
        log.error("Ad HTML retrieval failed: "+str(e))
    return innerHTML


def switch_to_frame_context(driver, iframe):
    # switch to iframe context
    for i in range(0, 3):
        try:
            iframeID = iframe.get_attribute('id')
            driver.switch_to.frame(iframeID)
            break
        except:
            log.warning('Element access attempt: ' + str(i))



def getRevContentAds(driver):

    # rev content ads appear as
    #revContent = driver.find_elements_by_xpath("//div[@id=rc-row-container]")

    revItems = driver.find_elements_by_class_name('rc-item')
    i = 0
    for item in revItems:

        image = item.find_element_by_class_name('rc-photo-container')
        text = item.text

        screenshotName = 'adScreenshots/rev' + str(i) + '.png'
        image.screenshot(screenshotName)

        i = i + 1

def extractEmbeddedUrl(compositeLink):

    #ignore the start of the url
    #We are looking for any urls within composite link
    protocol = "https"
    protocolLen = len(protocol)

    endDilimiter = '%'
    searchExpression = protocol + '://(.*?)' + endDilimiter
    #use inbuilt function, ignore the protocol at the start of the string
    found = re.search(searchExpression, compositeLink[protocolLen:])

    try:
        return found.group(1)
    except:
        return None

# Convert png string to Image Object for file upload and saving
def imageProcessing(png):
    buffer = io.BytesIO(png)
    # PIL image creation
    img = Image.open(buffer)

    #dimensions (width, height)
    w1, h1 = img.size
    w2, h2= math.floor(w1 * 0.7), math.floor(h1 * 0.7)

    ratio = h1 / w1

    # resize height proportion to new width
    newWidth = w2
    hsize = math.floor(newWidth * ratio)
    img = img.resize((newWidth, hsize), Image.ANTIALIAS)

    # second buffer
    #buf2 = io.BytesIO()

    #write to buffer
    #img.save(buf2, "png", quality=50, optimize=True)

    #attach name to object
    #buf2.name = 'ad.png'

    try:
        img.save('ad.png', quality=50, optimize=True)
    except IOError:
        log.error("could not access local disk for screenshot write")
        return

    try:
        # create file stream
        f = open("ad.png", "rb")
    except IOError:
        log.error("could not access local disk for screenshot read")
        return

    return f

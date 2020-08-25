from selenium.webdriver import Chrome
import re
from selenium import webdriver
from time import sleep
from random import seed, randint
import requests


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
            print('Element location not found or not visible')

        iframeID = switch_to_frame_context(driver, iframe)

        innerHTML = get_ad_html(driver, iframeID)

        adLink = find_ad_redirect(driver, iframeID)

        screenshotName = 'adScreenshots/google' + str(randint(0, 10000)) + '.png'

        driver.switch_to.default_content()
        try:
            base64_screenshot = iframe.screenshot_as_base64
        except:
            print('Screenshot capture failed')

        try:
            r = requests.post('http://db:8080/ads', data={
                "bot": bot.username, 
                "link": adLink, 
                "headline": adLink, 
                "html": innerHTML
            })
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('Screenshot saving failed')
            print(e.response.text)


    return screenshots


def find_ad_redirect(driver, iframeID):


    try:
        #adElem = driver.find_element_by_id(iframeID)

        # find the link embedded in the iframe
        linkElements = driver.find_elements_by_xpath(".//a[@href]")
    except:
        print('Cannot find internal link, check correct context is set')
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


def get_ad_html(driver, iframeID):
    innerHTML = None
    # Get ad html
    try:
        # innerHTML = driver.find_element_by_xpath(".//html[@*]").get_attribute('innerHTML')
        #adElem = driver.find_element_by_id(iframeID)
        innerHTML = driver.find_element_by_xpath(".//html[@*]").get_attribute('innerHTML')
    except:
        print("Ad HTML retrieval failed")
    return innerHTML


def switch_to_frame_context(driver, iframe):
    # switch to iframe context
    for i in range(0, 3):
        try:
            iframeID = iframe.get_attribute('id')
            driver.switch_to.frame(iframeID)
            break
        except:
            print('Element access attempt: ' + str(i))
    return iframeID


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
        print(image.screenshot_as_base64)
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



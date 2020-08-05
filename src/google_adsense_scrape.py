from selenium.webdriver import Chrome
import re
from selenium import webdriver
from time import sleep
from random import seed, randint


#given a selenium driver retrieves a list of google ads which appear on the page
def getGoogleAds(driver):
    seed(231)

    # google ads appear in iframes labelled as such
    iframes = driver.find_elements_by_xpath("//iframe[@data-google-container-id]")

    # Writing to a file
    adLinks = open('../../adLinks.txt', 'w')


    screenshots = []

    for iframe in iframes:

        try:
            iframe.location_once_scrolled_into_view
        except:
            print('Element location not found')


        for i in range(0,2):
            try:
                # Ad contents are dynamically loaded according to your cookie id
                # so we need to switch to that context
                driver.switch_to.frame(iframe)
                break
            except:
                print('Element access attempt: ' + str(i))

        try:


            #go down to the first Div in the iframe
            firstDiv = driver.find_element_by_xpath(".//div[@*]")

            #find the link embedded in the iframe
            linkElement = firstDiv.find_element_by_xpath(".//*[@href]")

            adLinks.write(
                (extractEmbeddedUrl(
                    linkElement.get_attribute('href'))
                )
            )
        except:
            print('Error in link')

        screenshotName = 'adScreenshots/google' + str(randint(0, 10000)) + '.png'

        driver.switch_to.default_content()
        try:
            iframe.screenshot(screenshotName)

            screenshots.append(iframe.screenshot_as_base64)
        except:
            print('Screenshot failed')

    return screenshots

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
        return 0



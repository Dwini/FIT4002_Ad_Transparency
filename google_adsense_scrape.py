from selenium.webdriver import Chrome
import re

#given a selenium driver retrieves a list of google ads which appear on the page
def getGoogleAds(driver):

    driver.switch_to.default_content()

    # google ads appear in iframes labelled as such
    iframes = driver.find_elements_by_xpath("//iframe[@data-google-container-id]")

    screenshots = []
    i = 0
    for iframe in iframes:

        screenshotName = 'adScreenshots/google' + str(i) + '.png'

        #Ad contents are dynamically loaded according to your cookie id
        #so we need to switch to that context
        driver.switch_to.frame(iframe)

        try:

            #go down to the first Div in the iframe
            firstDiv = driver.find_element_by_xpath(".//div[@*]")

            #find the link embedded in the iframe
            linkElement = firstDiv.find_element_by_xpath(".//*[@href]")

            print(linkElement.get_attribute('href'))
        except:
            print('Error in one or more links')


        try:
            iframe.screenshot(screenshotName)
            i = i + 1

            screenshots.append(iframe.screenshot_as_base64)
        except:
            print('one or more screenshots failed')

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


    searchExpression = protocol + '://' + '(.*)%'
    #use inbuilt function
    found = re.search(searchExpression, compositeLink[protocolLen:])

    try:
        return found.group(0)
    except:
        return 0

#For testing purposes only
webdriver = "chromedriver.exe"
driver = Chrome(webdriver)

url = "https://www.washingtonexaminer.com/"
driver.get(url)

getGoogleAds(driver)
getRevContentAds(driver)
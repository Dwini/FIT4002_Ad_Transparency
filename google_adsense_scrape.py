from selenium.webdriver import Chrome


#given a selenium driver retrieves a list of google ads which appear on the page
def getGoogleAds(driver):


    # google ads appear in iframes labelled as such
    iframes = driver.find_elements_by_xpath("//iframe[@data-google-container-id]")

    screenshots = []
    i = 0
    for iframe in iframes:
        try:
            screenshotName = 'adScreenshots/google' + str(i) + '.png'

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



#For testing purposes only
# webdriver = "chromedriver.exe"
# driver = Chrome(webdriver)
#
# url = "https://www.washingtonexaminer.com/"
# driver.get(url)
#
# getGoogleAds(driver)
# getRevContentAds(driver)
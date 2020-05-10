from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from time import sleep

webdriver = "chromedriver.exe"

driver = Chrome(webdriver)

url = "https://www.breitbart.com/"
driver.get(url)


sleep(30)

#google ads appear in iframes labelled as such
iframes = driver.find_elements_by_xpath("//iframe[@data-google-container-id]")


i = 0

for iframe in iframes:
    try:
        screenshotName = '/adScreenshots/' + str(i) + '.png'
        iframe.screenshot(screenshotName)
        i = i + 1
        print('saved')
        print(iframe.screenshot_as_base64)
    except:
        print('one or more screenshots failed')

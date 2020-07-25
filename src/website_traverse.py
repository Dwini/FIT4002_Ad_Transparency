from google_adsense_scrape import getGoogleAds
from random import seed, randint
from time import sleep
from selenium.webdriver import Chrome
from selenium import webdriver


# removes div such as notification or location requests
# TODO check if location dialogs should be confirmed
def clear_dialatogs(driver):

    #see if clicking main content will escape any popups


    dialogs = driver.find_elements_by_css_selector("[id*=dialog]")
    #TODO Can dialogs be encapsulated in classes?
    #dialogs_with_class = driver.find_elements_by_css_selector("[class*=dialog]")

    for dialog in dialogs:
        try:
            driver.execute_script("arguments[0].remove();", dialog)
        except:
            print('error in removing dialog')


webdriver = "chromedriver.exe"
driver = Chrome(webdriver)
#options = driver.ChromeOptions()
#options.add_argument("--start-maximized")
#driver = Chrome(chrome_options=options)

urls = open('urls.txt', 'r')

for url in urls:

    driver.get(url)

    #dialogues can get in the way of ads and scrolling
    sleep(randint(10, 15))
    clear_dialogs(driver)

    for i in range(3):
        sleep(randint(10, 15))
        driver.execute_script("window.scrollTo(0," + str(randint(50, 2000)) + ")")
        sleep(randint(1, 3))

    getGoogleAds(driver)
    sleep(2)


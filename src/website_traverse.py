from google_adsense_scrape import getGoogleAds
from random import random, randint
from time import sleep
from selenium.webdriver import Chrome


# removes div's that cause obstruction
def clear_dialogs(driver):

    # we want to be tracked
    # agree to any cookie requests
    accept_cookies(driver)

    # TODO see if clicking main content will escape any popups

    dialogs = driver.find_elements_by_css_selector("[id*=dialog]")

    #TODO Can dialogs be encapsulated in classes?
    #dialogs_with_class = driver.find_elements_by_css_selector("[class*=dialog]")

    for dialog in dialogs:
        try:
            driver.execute_script("arguments[0].remove();", dialog)
        except:
            print('error in removing dialog')


def accept_cookies(driver):

    agree_buttons = driver.find_elements_by_xpath(
        "//button[contains(string(), 'Agree') or contains(string(), 'Allow') or contains(string(), 'Accept')] ")
    for button in agree_buttons:
        try:
            button.click()
            sleep(random.random())
        except:
            print('Failed to click a button')


def click_local_links(driver):

    local_links = driver.find_elements_by_xpath("// a[not(contains(href, 'http'))]")

    for i in range(len(local_links)):
        try:
            if(isElementClickable):
                i = randint(0, len(local_links) - 1)
                print(local_links[i].location_once_scrolled_into_view)
                local_links[i].click()
                break
        except:
            print('Failed to click local link')

def isElementClickable(element):


    # is element visible by styles
    if (not element.isDisplayed):
        return False
    return True

    #TODO check if behind anything
    #
    # # is the element behind another element
    boundingRect = element.rect
    #
    # // adjust coordinates to get more accurate results
    # const left = boundingRect.left + 1;
    # const right = boundingRect.right - 1;
    # const top = boundingRect.top + 1;
    # const bottom = boundingRect.bottom - 1;
    #
    # if (document.elementFromPoint(left, top) !== element ||
    #     document.elementFromPoint(right, top) !== element ||
    #     document.elementFromPoint(left, bottom) !== element ||
    #     document.elementFromPoint(right, bottom) !== element) {
    #     return false;
    # }
    #
    # return true;
    # `;
    #
    # return element.getDriver().executeScript(SCRIPT, element);


webdriver = "chromedriver.exe"
driver = Chrome(webdriver)
#options = driver.ChromeOptions()
#options.add_argument("--start-maximized")
#driver = Chrome(chrome_options=options)

urls = open('urls.txt', 'r')


def random_wait_and_scroll(driver):
    # random wait and scroll action
    for i in range(3):
        sleep(randint(1, 3))
        driver.execute_script("window.scrollTo(0," + str(randint(50, 2000)) + ")")
        sleep(randint(1, 3))

#prevent them from getting in the way of ads
def remove_header(driver):

    headers = driver.find_elements_by_xpath("//div[contains(@class, 'header')] | //header[@class]")
    #//header[@class]" or
    for header in headers:
        try:
            driver.execute_script("arguments[0].remove();", header)
        except:
            print('error in removing dialog')

for url in urls:

    driver.get(url)
    sleep(randint(10, 15))

    #dialogues can get in the way of ads and scrolling
    clear_dialogs(driver)
    remove_header(driver)

    random_wait_and_scroll(driver)

    getGoogleAds(driver)

    click_local_links(driver)

    random_wait_and_scroll(driver)




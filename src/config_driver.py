# import external libraries.
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep


"""
Sets driver location to given lat/lon values.
    driver: Selenium driver
    location: Dictionary of the form { 'lat': ..., 'lon': ... }
"""
def set_location(driver, location):
    print('setting location (this will take a while)')
    # need to go to a web page so that bot can click on button to
    # use precise location
    driver.get("https://www.google.com/maps")

    # set location in selenium
    print('attempting to change location - method 1 of 2')
    sleep(10)
    driver.execute_cdp_cmd("Page.setGeolocationOverride", {
        "latitude": location['lat'],            # 32.585,       lat/lon for Warner Robins, 
        "longitude": location['lon'],           # -83.611,      Georgia, USA
        "accuracy": 100
    })

    driver.get("https://www.google.com/maps")

    print('attempting to change location - method 2 of 2')
    sleep(10)
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success) {" +
        "var position = {\"coords\" : {\"latitude\": \"%s\",\"longitude\": \"%s\"}};" % (location['lat'], location['lon']) +
        "success(position);}")

    driver.execute_script("var positionStr=\"\";" +
        "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
        "return positionStr;")

    print('finalising (almost done)')
    driver.get("https://www.google.com/maps")
    sleep(3)

    # click button to use precise location
    # eqQYZc is the id for the button, but need to be aware that
    # this may change at any time
    driver.get('https://google.com/search?q=google')
    driver.find_element_by_id('eqQYZc').click()
    sleep(3)

"""
Set up selenium driver with given proxy
"""
def setup_driver(proxyIP=None):
    # define options.
    print('setting options for session')
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    if proxyIP is not None:
        print('setting proxy %s' % proxyIP)
        chrome_options.add_argument('--proxy-server=%s' % proxyIP)

    print('building session...', end='')
    session = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    print('success')

    return session
# import external libraries.
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import geopy
from geopy.geocoders import Nominatim
import proxy

"""
Sets driver location to given lat/lon values.
    driver: Selenium driver
    location: Dictionary of the form { 'lat': ..., 'lon': ... }
"""
def set_location(driver, location):
    locator = Nominatim(user_agent="google")
    coordinates = "%f, %f" % (location['lat'], location['lon'])
    loc_info = locator.reverse(coordinates)
    print('>> Attempting to change browser location to: %s' % loc_info.raw['display_name'])
    print(">> (this will take a while)")
    # need to go to a web page so that bot can click on button to
    # use precise location
    driver.get("https://www.google.com/maps")

    # set location in selenium
    print('>> Trying method 1 of 2')
    sleep(10)
    driver.execute_cdp_cmd("Page.setGeolocationOverride", {
        "latitude": location['lat'],            # 32.585,       lat/lon for Warner Robins, 
        "longitude": location['lon'],           # -83.611,      Georgia, USA
        "accuracy": 100
    })

    driver.get("https://www.google.com/maps")

    print('>> Trying method 2 of 2')
    sleep(10)
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success) {" +
        "var position = {\"coords\" : {\"latitude\": \"%s\",\"longitude\": \"%s\"}};" % (location['lat'], location['lon']) +
        "success(position);}")

    driver.execute_script("var positionStr=\"\";" +
        "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
        "return positionStr;")

    print('>> Finalising browser location change (almost done)')
    driver.get("https://www.google.com/maps")
    sleep(3)

    # click button to use precise location
    # 'Wprf1b' is the id for the button, but need to be aware that
    # this may change at any time.
    try:
        driver.get('https://google.com/search?q=google')
        sleep(2)
        print('>> Location as seen by Google: %s' % driver.find_elements_by_xpath('//span[@id="Wprf1b"]')[0].text)
    except:
        print('>> Could not confirm new location. Assuming location changed successfully')

"""
Set up selenium driver with given proxy
"""
def setup_driver(proxyIP=None):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if proxyIP is not None:
        chrome_options.add_argument('--proxy-server=%s' % proxyIP)

    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def setup_driver_with_proxy(pos):
    """
    Use this to setup driver with a list of possible proxies
    """
    i = 0
    proxies = proxy.get_closest_proxies(pos)
    session = None

    while not session and i < len(proxies):
        address = proxies[i]['address']
        print("\n>> Trying IP: %s (%d/%d)" % (address, i+1, len(proxies)))
        session = setup_driver(address)

        if not proxy.ip_check(session):
            session.quit()
            session = None
            i += 1
        
    if session:
        print(">> Proxy change successful (location: %s)" % proxies[i]['location'])
    else:
        print(">> Error: No working proxies found")
    
    return session

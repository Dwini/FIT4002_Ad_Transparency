# import external libraries.
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import geopy
from geopy.geocoders import Nominatim
import os

from driver_config import proxy

USE_PROXIES = os.getenv('USE_PROXIES') == "1"
LOAD_SESSION = os.getenv('LOAD_SESSION') == "1"
AD_USERNAME = os.getenv('AD_USERNAME')

"""
Sets driver location to given lat/lon values.
    driver: Selenium driver
    location: Dictionary of the form { 'lat': ..., 'lon': ... }
"""
def set_location(driver, location):
    locator = Nominatim(user_agent="google")
    coordinates = "%f, %f" % (location['lat'], location['lon'])
    loc_info = locator.reverse(coordinates)
    print('>> Attempting to change browser location')
    print('\t>> Spoofing location: %s' % loc_info.raw['display_name'])

    # These are three different methods to spoof location
    driver.execute_cdp_cmd("Page.setGeolocationOverride", {
        "latitude": location['lat'],            # 32.585,       lat/lon for Warner Robins, 
        "longitude": location['lon'],           # -83.611,      Georgia, USA
        "accuracy": 100
    })
    driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success) {" +
        "var position = {\"coords\" : {\"latitude\": \"%s\",\"longitude\": \"%s\"}};" % (location['lat'], location['lon']) +
        "success(position);}")
    driver.execute_script("var positionStr=\"\";" +
        "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
        "return positionStr;")

    # Click button to use precise location
    driver.get('https://google.com/search?q=google')
    sleep(2)
    try:
        location_btn = driver.find_elements_by_xpath('//a[@id="eqQYZc"]')[0]    # TODO: change how this works. id could change
        location_btn.click()
    except:
        pass
    sleep(2)
    
    # Attempt to confirm location change
    try: 
        print('\t>> Location as seen by Google: %s' % driver.find_elements_by_xpath('//span[@id="Wprf1b"]')[0].text)
    except:
        print('\t>> Could not confirm new location. Assuming location changed successfully')

def create_driver(proxyIP=None):
    """
    Set up selenium driver with given proxy
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36"')

    if proxyIP is not None:
        chrome_options.add_argument('--proxy-server=%s' % proxyIP)

    if LOAD_SESSION:
        print('>> Attempting to load previous session')
        
        chrome_options.add_argument('--user-data-dir=/app/out/profiles/'+AD_USERNAME)
        chrome_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome('./driver_config/chromedriver', options=chrome_options)
        
        print('\t>> Successfully loaded session')
        return driver
    
    return webdriver.Chrome('./chromedriver', options=chrome_options)

def setup(pos=None):
    if not USE_PROXIES:
        return create_driver()
    
    i = 0

    proxies = proxy.get_proxy_list()

    # uncomment to sort proxies by distance from pos
    # TODO: Switch this on an environment variable?
    # proxies = proxy.sort_by_location(proxies, pos)
    
    session = None

    while not session and i < len(proxies):
        address = proxies[i]
        print("\n>> Trying IP: %s (%d/%d)" % (address, i+1, len(proxies)), end='')
        session = create_driver(address)

        if not proxy.ip_check(session):
            session.quit()
            session = None
            i += 1
        
    if session:
        ip_info = proxy.ip_lookup(address)
        location = '%s, %s, %s' % (ip_info['city'], ip_info['region'], ip_info['country'])
        print(">> Proxy change successful (location: %s)" % location)
    else:
        print(">> Error: No working proxies found")
    
    return session
    
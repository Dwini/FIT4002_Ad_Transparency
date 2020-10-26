# import external libraries.
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os, sys
import logging


log = logging.getLogger()

# Linux 64-bit (container use)
GECKODRIVER_PATH = './driver/geckodriver'
# Windows 64-bit
# GECKODRIVER_PATH = './driver/geckodriver.exe'

"""
Set up Selenium with Geckodriver
"""
def create_firefox_driver(ip=None, pos=None):
    log.info('Creating Firefox driver')

    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.webdriver.enabled', False)
    profile.set_preference('useAutomationExtension', False)

    # Location spoofing
    if os.getenv('CHANGE_LOCATION') == '1':
        profile.set_preference('geo.prompt.testing', True)
        profile.set_preference('geo.prompt.testing.allow', True)
        profile.set_preference('geo.provider.testing', True)
        profile.set_preference('geo.provider.network.url', 'data:application/json,{"location":{"lat":%s,"lng":%s},"accuracy":100.0}' % (pos['lat'], pos['lon'] ))

    # For container builds, set firefox options to allow container mode.
    firefox_options = FirefoxOptions()
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        firefox_options.add_argument('-headless')

    profile.update_preferences()
    driver = webdriver.Firefox(
        executable_path='./driver/geckodriver.exe',
        firefox_profile=profile,
        desired_capabilities=DesiredCapabilities.FIREFOX,
        options=firefox_options
    )
    driver.set_window_position(0, 0)

    # selenium screenshot throws NS_ERROR_LOSS_OF_SIGNIFICANT_DATA if the resolution is too big.
    driver.maximize_window()
    log.info('window size: '+str(driver.get_window_size()))

    # TODO: Proxy support
    # See: https://www.selenium.dev/documentation/en/webdriver/http_proxies/

    return driver

def create_driver(ip=None, pos=None):
    #return create_firefox_driver(ip=ip, pos=pos)
    return create_chrome_driver(ip=ip, pos=pos)

def create_driver_with_proxy(pos):
    i = 0
    proxies = proxy.get_proxy_list()

    # uncomment to sort proxies by distance from pos
    # TODO: Switch this on an environment variable?
    # proxies = proxy.sort_by_location(proxies, pos)

    session = None

    while not session and i < len(proxies):
        address = proxies[i]
        log.info("Trying IP: %s (%d/%d)" % (address, i+1, len(proxies)))
        session = create_driver(ip=address, pos=pos)

        if not proxy.ip_check(session):
            session.quit()
            session = None
            i += 1

    if session == None:
        raise RuntimeError('No working proxies found')
        return

    ip_info = proxy.ip_lookup(address)
    location = '%s, %s, %s' % (ip_info['city'], ip_info['region'], ip_info['country'])
    log.info("Proxy change successful (location: %s)" % location)

    return session

def create_chrome_driver(ip=None, pos=None):
    chromeOptions = webdriver.ChromeOptions()
    dirname = os.path.dirname(__file__)
    user_data = os.path.join(dirname + "/profile")


    chromeOptions.add_argument("--user-data-dir=" + user_data)
    if os.getenv('HEADLESS') == 1:
        chromeOptions.add_argument("--headless")

    chromeOptions.add_experimental_option(
        'excludeSwitches',
        [
            'disable-background-networking',
            'disable-sync',
            'disable-translate',
            'disable-web-resources',
            'disable-default-apps',
            'disable-zero-browsers-open-for-tests',
            'disable-popup-blocking',
            'enable-automation',
            'test-type',
            'use-mock-keychain',
            'enable-blink-features',
            'no-first-run',
            'disable-client-side-phishing-detection',
            'disable-hang-monitor',
            'disable-prompt-on-repost',
            'enable-logging'

        ])


    DRIVER_PATH = os.getenv('DRIVER_PATH')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chromeOptions)

    #driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
     #                     "var position = {coords : {latitude:" + str(pos['lat']) + ", longitude:" + str(pos['lon']) + "}  }; success(position);}")

    set_location_in_chrome(driver, pos)

    return driver
# import external libraries.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import logging

import driver.proxy as proxy
from driver.session import get_session

log = logging.getLogger()

# Linux 64-bit (container use)
CHROMEDRIVER_PATH = './driver/chromedriver'
# Windows 32-bit
# CHROMEDRIVER_PATH = './driver/chromedriver.exe'

SESSION_PATH = './out/sessions/' + os.getenv('AD_USERNAME')

# Linux 64-bit (container use)
GECKODRIVER_PATH = './driver/geckodriver'
# Windows 64-bit
# GECKODRIVER_PATH = './driver/geckodriver.exe'

"""
Set up selenium driver with given proxy
"""
def create_chrome_driver(ip=None, pos=None):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu') # necessary for docker container.
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36"')
    chrome_options.add_argument('--user-data-dir=' + SESSION_PATH)

    # https://stackoverflow.com/questions/62889739/selenium-gives-timed-out-receiving-message-from-renderer-for-all-websites-afte
    chrome_options.add_argument('enable-automation')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # For proxies
    if ip is not None:
        chrome_options.add_argument('--proxy-server=' + ip)

    get_session()
    log.info('Creating Chrome driver')
    try:
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
        return driver
    except:
        log.warning('Failed to create driver. Trying again')
    
    get_session(delete_old=True)
    log.info('Creating driver - Attempt 2')
    try:
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
        return driver
    except:
        log.error('Failed to create driver')
        raise

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

    profile.update_preferences()
    driver = webdriver.Firefox(
        executable_path=GECKODRIVER_PATH,
        firefox_profile=profile, 
        desired_capabilities=DesiredCapabilities.FIREFOX
    )
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)

    # TODO: Proxy support
    # See: https://www.selenium.dev/documentation/en/webdriver/http_proxies/

    return driver

def create_driver(ip=None, pos=None):
    if os.getenv('BROWSER') == 'firefox':
        return create_firefox_driver(ip=ip, pos=pos)
    else:
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
    
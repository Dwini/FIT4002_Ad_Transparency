# import external libraries.
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os, sys
import logging

import driver.proxy as proxy
from driver.session import get_session

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
    profile.set_preference('browser.private.browsing.autostart', False)

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
        executable_path=GECKODRIVER_PATH,
        firefox_profile=profile,
        desired_capabilities=DesiredCapabilities.FIREFOX,
        options=firefox_options,
    )
    driver.set_window_position(0, 0)

    # selenium screenshot throws NS_ERROR_LOSS_OF_SIGNIFICANT_DATA if the resolution is too big.
    driver.maximize_window()
    log.info('window size: '+str(driver.get_window_size()))

    # TODO: Proxy support
    # See: https://www.selenium.dev/documentation/en/webdriver/http_proxies/

    return driver

def create_driver(ip=None, pos=None):
    return create_firefox_driver(ip=ip, pos=pos)

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

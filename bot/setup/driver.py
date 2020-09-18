# import external libraries.
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import geopy
import os
import logging
import stat
import requests
import zipfile

import setup.proxy as proxy

LOGGER = logging.getLogger()

CHROMEDRIVER_PATH = './setup/chromedriver'

ALL_SESSIONS_PATH = './out/sessions/'
SESSION_PATH = ALL_SESSIONS_PATH + os.getenv('AD_USERNAME')
INITIAL_SESSION_PATH = './setup/initial_sessions/' + os.getenv('AD_USERNAME') + '.zip'

def get_session():
    if os.path.isdir(SESSION_PATH):
        LOGGER.info('Session data already exists. No need to extract')
        return

    if not os.path.isfile(INITIAL_SESSION_PATH):
        LOGGER.warning('No inital session data found, new session data will be created')
        LOGGER.warning('This will most likely raise a captcha on login')
        return

    LOGGER.info('Extracting session data')
    zipfile.ZipFile(INITIAL_SESSION_PATH, 'r').extractall(ALL_SESSIONS_PATH)

def create_driver(proxyIP=None):
    """
    Set up selenium driver with given proxy
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36"')
    chrome_options.add_argument('--user-data-dir=' + SESSION_PATH)
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if proxyIP is not None:
        chrome_options.add_argument('--proxy-server=%s' % proxyIP)
    
    LOGGER.info('Creating driver')
    try:
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    except:
        LOGGER.error('Failed to create driver')
        raise

    return driver

def get_driver(pos=None):
    get_session()

    if os.getenv('USE_PROXIES') != "1":
        return create_driver()
    
    i = 0
    proxies = proxy.get_proxy_list()

    # uncomment to sort proxies by distance from pos
    # TODO: Switch this on an environment variable?
    # proxies = proxy.sort_by_location(proxies, pos)
    
    session = None

    while not session and i < len(proxies):
        address = proxies[i]
        LOGGER.info("Trying IP: %s (%d/%d)" % (address, i+1, len(proxies)))
        session = create_driver(address)

        if not proxy.ip_check(session):
            session.quit()
            session = None
            i += 1

    if session == None:
        LOGGER.error("No working proxies found")
        raise RuntimeError('No working proxies found')
        return
        
    ip_info = proxy.ip_lookup(address)
    location = '%s, %s, %s' % (ip_info['city'], ip_info['region'], ip_info['country'])
    LOGGER.info("Proxy change successful (location: %s)" % location)    
    return session
    
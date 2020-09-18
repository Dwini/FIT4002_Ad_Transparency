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
BASE_URL = 'https://fit4002.s3-ap-southeast-2.amazonaws.com/session/'

CHROMEDRIVER_URL = BASE_URL + 'chromedriver'
CHROMEDRIVER_PATH = './out/chromedriver'

SESSION_URL = BASE_URL + os.getenv('AD_USERNAME') + '.zip'
PROFILES_PATH = './out/profiles/'
SESSION_PATH = PROFILES_PATH + os.getenv('AD_USERNAME')

def get_session():
    if os.path.isdir(SESSION_PATH):
        LOGGER.info('Session data already exists. No need to download')
        return

    LOGGER.info('Downloading session data')
    r = requests.get(SESSION_URL, allow_redirects=True)
    r.raise_for_status()
    open(SESSION_PATH + '.zip', 'wb').write(r.content)

    LOGGER.info('Extracting session data')
    zipfile.ZipFile(SESSION_PATH + '.zip', 'r').extractall(PROFILES_PATH)

def download_chromedriver():
    if os.path.isfile(CHROMEDRIVER_PATH):
        LOGGER.info('"chromedriver" already exists. No need to download')
        return

    LOGGER.info('Downloading "chromedriver"')
    r = requests.get(CHROMEDRIVER_URL, allow_redirects=True)
    r.raise_for_status()
    open(CHROMEDRIVER_PATH, 'wb').write(r.content)

    st = os.stat(CHROMEDRIVER_PATH)
    os.chmod(CHROMEDRIVER_PATH, st.st_mode | stat.S_IEXEC)

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
    download_chromedriver()
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
    
# import external libraries.
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import geopy
import os

import setup.proxy as proxy

USE_PROXIES = os.getenv('USE_PROXIES') == "1"
LOAD_SESSION = os.getenv('LOAD_SESSION') == "1"
AD_USERNAME = os.getenv('AD_USERNAME')

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
        driver = webdriver.Chrome('./setup/chromedriver', options=chrome_options)
        
        print('\t>> Successfully loaded session')
        return driver
    
    return webdriver.Chrome('./chromedriver', options=chrome_options)

def get_driver(pos=None):
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
    
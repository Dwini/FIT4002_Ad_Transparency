# import external libraries.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import logging

import driver.proxy as proxy

log = logging.getLogger()

CHROMEDRIVER_PATH = './driver/chromedriver'
# If running in Windows use this chromedriver instead
# CHROMEDRIVER_PATH = './driver/chromedriver.exe'

SESSION_PATH = './out/sessions/' + os.getenv('AD_USERNAME')

def create_driver(proxyIP=None):
    """
    Set up selenium driver with given proxy
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')   # necessary for docker container.
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36"')
    chrome_options.add_argument('--user-data-dir=' + SESSION_PATH)
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if proxyIP is not None:
        chrome_options.add_argument('--proxy-server=%s' % proxyIP)
    
    log.info('Creating driver')
    try:
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    except:
        log.error('Failed to create driver')
        raise

    return driver

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
        session = create_driver(address)

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
    
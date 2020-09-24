# import external libraries.
import requests
import urllib.request
import math
import json
from time import sleep
import logging

log = logging.getLogger()

# define constants.
HTTP_IP_CHECK_URL = 'http://httpbin.org/ip'
HTTPS_IP_CHECK_URL = 'https://httpbin.org/ip'
PROXY_REQUESL_URLS = [
    "https://api.proxyscrape.com/?request=getproxies&timeout=100&country=US&anonymity=elite&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&timeout=200&country=US&anonymity=elite&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&timeout=300&country=US&anonymity=elite&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&timeout=400&country=US&anonymity=elite&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&timeout=500&country=US&anonymity=elite&proxytype=http",
    "http://pubproxy.com/api/proxy?limit=5&format=txt&country=US&speed=1&type=http",
    "https://api.proxyscrape.com/?request=getproxies&timeout=1000&country=US&anonymity=elite&proxytype=http"
    # "http://pubproxy.com/api/proxy?limit=5&format=txt&country=US&speed=5&type=http",
    # "https://api.proxyscrape.com/?request=getproxies&timeout=5000&country=US&anonymity=elite&proxytype=http",
    # "http://pubproxy.com/api/proxy?limit=5&format=txt&country=US&speed=10&type=http"
]
URL_STEM = "http://ip-api.com/json/" # followed by IP Address w/o port number.

"""
Check if successfully connected to proxy server
Returns true if working, else false
"""
def ip_check(driver):
    try:
        # Connect to HTTP_IP_CHECK_URL and print URL to console.
        log.info('Connecting to '+HTTP_IP_CHECK_URL+' ...')
        driver.get(HTTP_IP_CHECK_URL)
        http_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]

        # TTODO - have both HTTP and HTTPS proxies... currently only have HTTP.
        # Connect to HTTPS_IP_CHECK_URL and print URL to console.
        # print('>> Connecting to '+HTTPS_IP_CHECK_URL+' ...', end="")
        # driver.get(HTTPS_IP_CHECK_URL)
        # https_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]
        # print("done. (response: %s)" % https_ip_address)

        return True
    except:
        log.warning("IP check failed")
        return False

"""
Input an IP Address (can include the port number) and return an object with the
country, region, city and zip code of the IP Address.
param: String in the form xxx.xxx.xxx or xxx.xxx.xxx:yy.
return object with {county, regionName, city, zip}
"""
def ip_lookup(ip_address):
    # remove the port number from the input.
    ip = ip_address.split(':')[0]

    # poll the api and return the object.
    r = requests.get(url=URL_STEM+ip)
    return r.json()

"""
Get list of proxies. These *should* be sorted fastest to slowest
"""
def get_proxy_list():
    log.info('Fetching list of proxies (this might take a while)')
    proxy_list = []

    for i, url in enumerate(PROXY_REQUESL_URLS):
        log.info('(%d/%d) Querying proxy list...' % (i+1, len(PROXY_REQUESL_URLS)))
        try:
            proxy_list += list(urllib.request.urlopen(url))
        except:
            pass

    result = [line.decode('utf-8').strip('\n').strip('\r') for line in proxy_list]
    result = list(set(result))
    log.info("%d proxies found" % len(result))

    return result

"""
Given a list of proxies and a position, sorts the proxies by distance.
position: dictionary in the form: { 'lat': ... , 'lon': ... }
"""
def sort_by_location(proxy_list, position):
    # list of dictionaries that contain ip and distance info
    results = []

    log.info('Starting proxy check (this might also take a while)')

    for i, ip in enumerate(proxy_list):
        log.info('\t>> (%d/%d) Fetching proxy info...' % (i+1, len(proxy_list)))
        try:
            ip_info = ip_lookup(ip)

            # basic way to check distance between 2 points
            dist = (position['lat'] - ip_info['lat'])**2 + (position['lon'] - ip_info['lon'])**2

            results.append({ 'address': ip, 'dist': dist })
        except:
            log.warning('Could not fetch proxy info')
            sleep(5)
            pass

    log.info('%s possible working proxies found' % len(results))

    # sort proxies by distance
    return [p['address'] for p in sorted(results, key=lambda k: k['dist'])]
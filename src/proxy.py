# import external libraries.
import requests
import urllib.request
import math
import json

# define constants.
HTTP_IP_CHECK_URL = 'http://httpbin.org/ip'
HTTPS_IP_CHECK_URL = 'https://httpbin.org/ip'
# HTTP_PROXIES = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=elite"
HTTP_PROXIES = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=US&ssl=all&anonymity=elite"
URL_STEM = "http://ip-api.com/json/" # followed by IP Address w/o port number.

"""
Check if successfully connected to proxy server
Returns true if working, else false
"""
def ip_check(driver):
    print('checking ip...')

    try:
        # Connect to HTTP_IP_CHECK_URL and print URL to console.
        print('connecting to '+HTTP_IP_CHECK_URL+' ...')
        driver.get(HTTP_IP_CHECK_URL)
        http_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]

        # Connect to HTTPS_IP_CHECK_URL and print URL to console.
        #print('connecting to '+HTTPS_IP_CHECK_URL+' ...')
        #driver.get(HTTPS_IP_CHECK_URL)
        #https_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]

        print("connected to proxy")
        return True
    except:
        print("could not connect to proxy")
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
Given a postion, finds the closest proxy server.

position: dictionary in the form: { 'lat': ... , 'lon': ... }
"""
def get_closest_proxies(position):
    print('finding closest proxy...')

    # list of dictionaries that contain ip and distance info
    results = []

    proxy_list = list(urllib.request.urlopen(HTTP_PROXIES))
    num_failed = 0
    num_proxies = len(proxy_list)

    for i in range(num_proxies):
        # decode line in file
        ip = proxy_list[i].decode('utf-8').strip('\n').strip('\r')

        # get location and other info for proxy
        try:
            print("querying info for proxy: %s (%s/%s) ..." % (ip, i+1, num_proxies), end='')
            ip_info = ip_lookup(ip)
        except:
            print(" failed")
            num_failed += 1
            continue

        print(" success")

        # very basic way to check distance between 2 points
        dist = (position['lat'] - ip_info['lat'])**2 + (position['lon'] - ip_info['lon'])**2

        results.append({ 'ip': ip, 'dist': dist })

    print("\ndone. %s proxies failed" % num_failed)

    # sort list of dicts
    sorted_proxies = sorted(results, key=lambda k: k['dist'])

    # get ips, discard dists
    return [ p['ip'] for p in sorted_proxies ]

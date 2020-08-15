# import external libraries.
import requests
import urllib.request
import math
import json

# define constants.
HTTP_IP_CHECK_URL = 'http://httpbin.org/ip'
HTTPS_IP_CHECK_URL = 'https://httpbin.org/ip'
HTTP_PROXIES = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=elite"
# HTTP_PROXIES = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=US&ssl=all&anonymity=elite"
URL_STEM = "http://ip-api.com/json/" # followed by IP Address w/o port number.

"""
Check if successfully connected to proxy server
Returns true if working, else false
"""
def ip_check(driver):    
    try:
        # Connect to HTTP_IP_CHECK_URL and print URL to console.
        print('>> Connecting to '+HTTP_IP_CHECK_URL+' ...', end="")
        driver.get(HTTP_IP_CHECK_URL)
        http_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]
        print("done. (response: %s)" % http_ip_address)

        # Connect to HTTPS_IP_CHECK_URL and print URL to console.
        print('>> Connecting to '+HTTPS_IP_CHECK_URL+' ...', end="")
        driver.get(HTTPS_IP_CHECK_URL)
        https_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]
        print("done. (response: %s)" % https_ip_address)

        return True
    except:
        print("failed")
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
    print('>> Fetching list of proxies...')

    # list of dictionaries that contain ip and distance info
    results = []

    proxy_list = list(urllib.request.urlopen("http://pubproxy.com/api/proxy?limit=20&format=txt&http=true&country=US&type=http&https=true"))
    proxy_list = proxy_list + list(urllib.request.urlopen(HTTP_PROXIES))

    num_total = len(proxy_list)
    print(">> Found %d proxies" % num_total)

    for line in proxy_list:
        # decode line in file
        ip = line.decode('utf-8').strip('\n').strip('\r')
        
        # get location and other info for proxy
        try:
            print(">> Querying proxy: %s ..." % ip, end='')
            ip_info = ip_lookup(ip)
        except:
            print("failed")
            continue

        print("success")

        # very basic way to check distance between 2 points
        dist = (position['lat'] - ip_info['lat'])**2 + (position['lon'] - ip_info['lon'])**2

        results.append({ 
            'address': ip, 
            'dist': dist, 
            'location': '%s, %s, %s' % (ip_info['city'], ip_info['region'], ip_info['country']) 
        })

    print(">> Proxy check complete. %s possible working proxies found" % len(results))

    # sort list of dicts
    return sorted(results, key=lambda k: k['dist'])
# import external libraries.
import requests
import urllib.request
import math

# define constants.
HTTP_PROXIES = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=elite"
URL_STEM = "http://ip-api.com/json/" # followed by IP Address w/o port number.

"""
Input an IP Address (can include the port number) and return an object with the
country, region, city and zip code of the IP Address.
param: String in the form xxx.xxx.xxx or xxx.xxx.xxx:yy.
return object with {county, regionName, city, zip}
"""
def ip_location_lookup(ip_address):
    # remove the port number from the input.
    ip = ip_address.split(':')[0]

    # poll the api and return the object.
    r = requests.get(url=URL_STEM+ip)
    return r.json()

"""
Given a postion, finds the closest proxy server.
'position' is dictionary in the form of: { 'lat': ... , 'lon': ... } 
"""
def get_closest_ip(position):
    min_dist = None
    min_ip = None

    for line in urllib.request.urlopen(HTTP_PROXIES):
        # decode line in file
        ip = line.decode('utf-8').strip('\n').strip('\r')
        
        # get location and other info for ip
        try:
            print("querying info for IP: %s ..." % ip, end='')
            ip_info = ip_location_lookup(ip)
        except:
            print(" failed")
            continue

        print(" success")

        # compare distance ()
        dist = (position['lat'] - ip_info['lat'])**2 + (position['lon'] - ip_info['lon'])**2
        if min_dist == None or dist < min_dist:
            min_dist = dist
            min_ip = ip
    
    return min_ip


# test function.
if __name__ == '__main__':
    # test addresses.

    # test_ip_addresses = ['12.139.101.100:80', '50.250.75.153', '69.65.65.178', \
    #     '50.204.122.174:54321']

    # iterate over each address and print the zip code.

    # for ip in test_ip_addresses:
    #     print(ip+': '+ip_location_lookup(ip)['zip'])

    # define dummy position (somewhere in Georgia)
    position = { 'lat': 30.7948526, 'lon': -86.6827337 }

    # find the closest proxy server
    min_ip = get_closest_ip(position)
    print("\nIP with min distance: " + min_ip)
# import external libraries.
import requests

# define constants.
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

# test function.
if __name__ == '__main__':
    # test addresses.
    test_ip_addresses = ['12.139.101.100:80', '50.250.75.153', '69.65.65.178', \
        '50.204.122.174:54321']

    # iterate over each address and print the zip code.
    for ip in test_ip_addresses:
        print(ip+': '+ip_location_lookup(ip)['zip'])

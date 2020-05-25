"""
Entry point of the container.
"""
# import external libraries.
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# define constants.
HTTP_IP_CHECK_URL = 'http://httpbin.org/ip'
HTTPS_IP_CHECK_URL = 'https://httpbin.org/ip'

print('starting selenium')

# load google in selenium
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Connect to HTTP_IP_CHECK_URL and print URL to console.
print('connecting to '+HTTP_IP_CHECK_URL)
driver.get(HTTP_IP_CHECK_URL)
http_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]
print("HTTP IP: "+http_ip_address)

# Connect to HTTPS_IP_CHECK_URL and print URL to console.
print('connecting to '+HTTPS_IP_CHECK_URL)
driver.get(HTTPS_IP_CHECK_URL)
https_ip_address = json.loads(driver.find_element_by_tag_name("body").text)["origin"]
print("HTTPS IP: "+https_ip_address)

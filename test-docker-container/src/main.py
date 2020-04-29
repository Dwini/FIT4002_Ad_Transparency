"""
Entry point of the container.
"""
# import external libraries.
import requests

# define constants
URL = 'https://www.aemo.com.au/aemo/apps/api/report/ELEC_NEM_SUMMARY'
HEADERS = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}

#
r = requests.get(url=URL, headers=HEADERS)
print(r.json())

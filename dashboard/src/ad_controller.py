"""
This module handles the downloading and parsing of ad information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 30/09/2020 - refactor to handle db retrieval.
"""
# import external libraries.
import requests
from datetime import datetime

# import local modules.
from src import cache_handler

"""
This function will update the cached ad list. Each element in the list is an
object holding advertisement information.
"""
def update_ad_cache():
    # clear the currently cached list of ads.
    cache_handler.ad_dict.clear()

    # retrieve all raw data from 'Ads' table in AWS DynamoDB.
    data = get_ad_table()

    # iterate over each item in the raw data and append the information to the
    # the ad_dict.
    for ad in data:
        # parse data and add to ad_dict. set id as the key and create an
        # object as the value.
        cache_handler.ad_dict[ad['id']] = {
            'bot': ad['bot'] if 'bot' in ad else '-',
            'datetime': ad['datetime'] if 'datetime' in ad else '-',
            'file': ad['file'] if 'file' in ad else '-',
            'link': ad['link'] if 'link' in ad else '-',
            'logged_in': ad['logged_in'] if 'logged_in' in ad else '-',
            'current_page': ad['current_page'] if 'current_page' in ad else '-',
        }

"""
Return a full dump of the bot table. This will need to be parsed by the caller.
"""
def get_ad_table():
    # format current date for to pass to endpoint.
    date_string = datetime.now().strftime('%d-%m-%Y')

    # connect to db project and return the db data.
    r = requests.get(cache_handler.db_uri+'/ads?date='+date_string)

    # return the json data.
    return r.json()

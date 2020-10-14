"""
This module handles the downloading and parsing of error information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 30/09/2020 - create module from error_controller.py as a template.
"""
# import external libraries.
import requests
from datetime import datetime, date, timedelta

# import local modules.
from src import cache_handler

"""
This function will update the cached error dictionary. Each key in the dictionary
is the name of the log file where this error occurred and the corresponding value
is an object holding error information.
"""
def update_log_cache():
    # clear the currently cached list of bots.
    cache_handler.log_dict.clear()

    # format dates to pass db to endpoint.
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # retrieve all raw data from 'Errors' table in AWS DynamoDB.
    data = get_log_table(today.strftime('%Y.%m.%d'))
    data = data + get_log_table(yesterday.strftime('%Y.%m.%d'))
    data = data + get_log_table(tomorrow.strftime('%Y.%m.%d'))

    # iterate over each item in the raw data and append the information to the
    # the log_dict.
    for log in data:
        # parse data and add to log_dict. set filename as the key and
        # create an object as the value.
        cache_handler.log_dict[log['filename']] = {
            'link': log['link'],
            'time': datetime.strptime(log['filename'][:19], '%Y.%m.%d_%H.%M.%S'),
            'bot': log['filename'][20:].replace('.log', '')
        }

"""
Return a full dump of the log table. This will need to be parsed by the caller.
"""
def get_log_table(date_string):
    # connect to db project and return the db data.
    r = requests.get(cache_handler.db_uri+'/logs?prefix='+date_string)

    # return the json data.
    return r.json()

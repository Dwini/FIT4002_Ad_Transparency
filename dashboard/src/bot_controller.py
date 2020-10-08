"""
This module handles the downloading and parsing of bot information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 30/09/2020 - refactor to handle db retrieval.
"""
# import external libraries.
import requests

# import local modules.
from src import cache_handler, search_term_controller

"""
This function will update the cached bot dictionary. Each key in the dictionary
is a bot username and the corresponding value is an object holding bot information.
"""
def update_bot_cache():
    # clear the currently cached list of bots.
    cache_handler.bot_dict.clear()

    # retrieve all raw data from 'Bots' table in AWS DynamoDB.
    bot_data = get_bot_table()

    # retrieve all raw data from 'Status' table in AWS DynamoDB.
    status_data = get_bot_status_table()

    # iterate over each item in the raw data and append the information to the
    # the bot_list.
    for bot in bot_data:
        # parse data and add to bot_dict. set username as the key and create an
        # object as the value.
        cache_handler.bot_dict[bot['username']] = {
            'password': bot['password'],
            'name': bot['name'][0]+" "+bot['name'][1],
            'gender': bot['gender'] if 'gender' in bot else '-',
            'political_ranking': int(bot['political_ranking']),
            'other_terms_category': int(bot['other_terms_category']) if 'other_terms_category' in bot else '-',
            'dob': bot['DOB'] if 'DOB' in bot else '-',
            'latitude': float(bot['location']['latitude']) if 'location' in bot else '-',
            'longitude': float(bot['location']['longitude']) if 'location' in bot else '-',
            'status': status_data[bot['username']] if bot['username'] in status_data else 'Unknown',
        }

    # once bot data has been saved, load search terms.
    search_term_controller.update_political_cache()
    search_term_controller.update_other_cache()

"""
Return a full dump of the bot table. This will need to be parsed by the caller.
"""
def get_bot_table():
    # connect to db project and return the db data.
    r = requests.get(cache_handler.db_uri+'/bots')

    # return the json data.
    return r.json()

"""
Return a full dump of the bot table. This will need to be parsed by the caller.
"""
def get_bot_status_table():
    # connect to db project and return the db data.
    r = requests.get(cache_handler.db_uri+'/bot_scheduler/statuses')

    # return the json data.
    return r.json()

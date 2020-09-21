"""
This module handles the downloading and parsing of bot information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 8/09/2020 - create module.
"""
# import local modules.
from src import db_controller, cache_handler

"""
This function will update the cached bot dictionary. Each key in the dictionary
is a bit username and the corresponding value is an object holding bot information.
"""
def update_bot_cache():
    # clear the currently cached list of bots.
    cache_handler.bot_dict.clear()

    # retrieve all raw data from 'Bots' table in AWS DynamoDB.
    data = db_controller.get_bot_table()

    # iterate over each item in the raw data and append the information to the
    # the bot_list.
    for bot in data:
        # parse data and add to bot_dict. set username as the key and create an
        # object as the value.
        cache_handler.bot_dict[bot['username']] = {
            'password': bot['password'],
            'name': bot['name'][0]+" "+bot['name'][1],
            'gender': bot['gender'] if 'gender' in bot else '-',
            'political_ranking': int(bot['political_ranking']),
            'dob': bot['DOB'] if 'DOB' in bot else '-',
            'latitude': float(bot['location']['latitude']) if 'location' in bot else '-',
            'longitude': float(bot['location']['longitude']) if 'location' in bot else '-',
        }

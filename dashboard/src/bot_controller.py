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
    raw_data = db_controller.get_full_table('Bots')

    # iterate over each item in the raw data and append the information to the
    # the bot_list.
    for item in raw_data['Items']:
        # parse data and add to bot_dict. set username as the key and create an
        # object as the value.
        cache_handler.bot_dict[item['username']['S']] = {
            'password': item['password']['S'],
            'name': item['name']['L'][0]['S']+" "+item['name']['L'][1]['S'],
            'gender': item['gender']['S'] if 'gender' in item else '-',
            'political_ranking': int(item['political_ranking']['N']),
            'dob': item['DOB']['S'] if 'DOB' in item else '-',
            'latitude': float(item['location']['M']['latitude']['N']) if 'location' in item else '-',
            'longitude': float(item['location']['M']['longitude']['N']) if 'location' in item else '-',
        }

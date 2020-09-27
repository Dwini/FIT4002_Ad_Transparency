"""
This module handles the downloading and parsing of error information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 27/09/2020 - create module.
"""
# import local modules.
from src import db_controller, cache_handler, search_term_controller

"""
This function will update the cached bot dictionary. Each key in the dictionary
is a bit username and the corresponding value is an object holding bot information.
"""
def update_error_cache():
    # clear the currently cached list of bots.
    cache_handler.error_dict.clear()

    # retrieve all raw data from 'Errors' table in AWS DynamoDB.
    data = db_controller.get_error_table()

    # iterate over each item in the raw data and append the information to the
    # the bot_list.
    for error in data:
        # parse data and add to error_dict. set log_file name as the key and
        # create an object as the value.
        cache_handler.error_dict[error['log_file']] = {
            'message': error['message'],
            'link': error['link']
        }

"""
This module handles the downloading and parsing of error information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 30/09/2020 - refactor to handle db retrieval.
"""
# import external libraries.
import requests

# import local modules.
from src import cache_handler, search_term_controller

"""
This function will update the cached error dictionary. Each key in the dictionary
is the name of the log file where this error occurred and the corresponding value
is an object holding error information.
"""
def update_error_cache():
    # clear the currently cached list of bots.
    cache_handler.error_dict.clear()

    # retrieve all raw data from 'Errors' table in AWS DynamoDB.
    data = get_error_table()

    # iterate over each item in the raw data and append the information to the
    # the bot_list.
    for error in data:
        # parse data and add to error_dict. set log_file name as the key and
        # create an object as the value.
        cache_handler.error_dict[error['log_file']] = {
            'message': error['message'],
            'link': error['link']
        }

"""
This function will remove the error from the cache dictionary and remove it from
the db by sending a post request to the db project.
"""
def remove_error(log_file):
    # if this log_file is not in the error_dict, returnwithout doing anything.
    if log_file not in cache_handler.error_dict:
        return

    # delete the file from the error_dict.
    del cache_handler.error_dict[log_file]

    # send a delete request to the db.
    r = requests.delete(cache_handler.db_uri+'/error/'+log_file)

    # check if successful.
    if r.status_code == 200:
        print('deleted error successfully: '+log_file)
    else:
        print('delete error failed: '+log_file)

"""
Return a full dump of the error table. This will need to be parsed by the caller.
"""
def get_error_table():
    # connect to db project and return the db data.
    r = requests.get(cache_handler.db_uri+'/errors')

    # return the json data.
    return r.json()

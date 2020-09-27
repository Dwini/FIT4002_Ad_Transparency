"""
This module handles the retrieval of data from the dynamodb instance on AWS.
Each function retrieves raw data which will be parsed by specific modules.

Last updated: MB 21/09/2020 - connect to NodeJS DB project instead of making connection
                                directly to DynamoDB.
"""
# import external libraries.
import os, dotenv, requests, time
dotenv.load_dotenv()

# import local modules.
from src import cache_handler

# load constants.
DB_URI = os.getenv('DB_URI') or 'http://localhost:8080'  # default db project endpoint.

"""
Return a full dump of the bot table. This will need to be parsed by the caller.
"""
def get_bot_table():
    # connect to db project and return the db data.
    r = requests.get(DB_URI+'/bots')

    # return the json data.
    return r.json()

"""
Return a full dump of the bot table. This will need to be parsed by the caller.
"""
def get_ad_table():
    # connect to db project and return the db data.
    r = requests.get(DB_URI+'/ads')

    # return the json data.
    return r.json()

"""
Return a full dump of the error table. This will need to be parsed by the caller.
"""
def get_error_table():
    # connect to db project and return the db data.
    r = requests.get(DB_URI+'/errors')

    # return the json data.
    return r.json()

"""
Save a json list of political search terms for this other ranking into cache.
"""
def save_political_search_terms(ranking):
    # connect to the db project and return the political searchterms.
    r = requests.get(DB_URI+'/search_terms/political/'+str(ranking))

    # try and parse the data.
    try:
        # parse into json.
        data = r.json()

        # override the old list with the new list.
        cache_handler.political_search_term_dict[ranking] = data

    # if error, do nothing.
    except:
        pass

"""
Save a json list of other search terms for this other ranking into cache.
"""
def save_other_search_terms(ranking):
    # connect to the db project and return the other searchterms.
    r = requests.get(DB_URI+'/search_terms/other/'+str(ranking))

    # try and parse the data.
    try:
        # parse into json.
        data = r.json()

        # override the old list with the new list.
        cache_handler.other_search_term_dict[ranking] = data

    # if error, do nothing.
    except:
        pass

"""
Block execution of this thread until the DB Project has been found.
"""
def wait_for_heartbeat():
    # Do not execute until db container has been started.
    response = None
    attempts = 0
    while response is None and attempts < 10:
        attempts += 1
        # attempt to connect.
        try:
            response = requests.get(DB_URI+'/heartbeat')
            print('found db project...')

        # if no connection, wait 10 seconds and try again.
        except:
            print('no response from db project. attempt: '+str(attempts))
            time.sleep(10)

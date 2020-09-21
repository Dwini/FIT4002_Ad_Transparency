"""
This module handles the retrieval of data from the dynamodb instance on AWS.
Each function retrieves raw data which will be parsed by specific modules.

Last updated: MB 21/09/2020 - connect to NodeJS DB project instead of making connection
                                directly to DynamoDB.
"""
# import external libraries.
import os, dotenv, requests, time
dotenv.load_dotenv()

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

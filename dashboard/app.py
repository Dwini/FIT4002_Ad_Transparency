"""
This is the main application for the Ad Transparency Dashboard project. It will
link routes files and provide an entrypoint for gunicorn.

Last updated: MB 27/09/2020 - load errors from DynamoDB into a cache on startup.
"""
# import external libraries.
import os, sys, json, requests, time
from flask import Flask, request, abort

# import local modules.
from src import bot_controller, ad_controller, error_controller, cache_handler, log_controller

# import routes.
from routes import index, bots, ads, search_terms, errors, logs

# define constants.
FILENAME = os.path.basename(__file__)

# define app.
app = Flask(__name__, template_folder='public/templates', static_folder='public/static')

# initialise routes.
index.init(app)
bots.init(app)
ads.init(app)
search_terms.init(app)
errors.init(app)
logs.init(app)

# Do not execute until db container has been started.
response = None
attempts = 0
while response is None and attempts < 10:
    attempts += 1
    # attempt to connect.
    try:
        response = requests.get(cache_handler.db_uri+'/heartbeat')
        print('found db project...')

    # if no connection, wait 10 seconds and try again.
    except:
        print('no response from db project. attempt: '+str(attempts))
        time.sleep(10)

# populate the bot and ad caches.
print('loading data into cache...')
bot_controller.update_bot_cache()
print('finished loading bot cache...')
ad_controller.update_ad_cache()
print('finished loading ad cache...')
error_controller.update_error_cache()
print('finished loading error cache...')
log_controller.update_log_cache()
print('finished loading log cache...')

# called on startup.
if __name__ == "__main__":
    # retrieve hostname and port from arguments.
    args = sys.argv

    # start the GEM server in a dedicated process.
    host = args[1] if len(args)>2 else '0.0.0.0'
    port = args[2] if len(args)>3 else int(os.environ.get('PORT', 5000))
    app.run(host = host, port = port)

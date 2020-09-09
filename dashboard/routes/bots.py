"""
Called by app.py when `/bots` route is called.

Last updated: MB 9/09/2020 - added caching functionality.
"""
# import external libraries.
import os
from flask import render_template, request

# import local modules.
from src import bot_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve new bot information from DynamoDB if 'refresh'
    parameter is True. Otherwise use the currently cached bot data.
    """
    @app.route("/bots", methods=['GET'])
    def botDashboard():
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload bot information into the cache.
        if refresh is True:
            print('refresh bots')
            bot_controller.update_bot_cache()

        # render the bot template with current cached data.
        return render_template('pages/botDashboard.html', data={**cache_handler.render_dict, **{
            'bots': cache_handler.bot_dict,
        }})

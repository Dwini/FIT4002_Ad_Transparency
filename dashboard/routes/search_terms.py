"""
Called by app.py when political or other search terms are viewd.

Last updated: MB 21/09/2020 - created module.
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
    parameter is True. Otherwise use the currently cached political search
    term data.
    """
    @app.route("/political/<int:ranking>", methods=['GET'])
    def politicalDashboard(ranking):
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload bot information into the cache.
        if refresh is True:
            print('refresh bots')
            bot_controller.update_bot_cache()

        # render the bot template with current cached data.
        return render_template('pages/politicalDashboard.html', data={**cache_handler.render_dict, **{
            'political_search_terms': cache_handler.political_search_term_dict[ranking] if ranking in cache_handler.political_search_term_dict else [],
        }})

    """
    Called by app.py. Retrieve new bot information from DynamoDB if 'refresh'
    parameter is True. Otherwise use the currently cached other search
    term data.
    """
    @app.route("/other/<int:ranking>", methods=['GET'])
    def otherDashboard(ranking):
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload bot information into the cache.
        if refresh is True:
            print('refresh bots')
            bot_controller.update_bot_cache()

        # render the bot template with current cached data.
        return render_template('pages/otherDashboard.html', data={**cache_handler.render_dict, **{
            'other_search_terms': cache_handler.other_search_term_dict[ranking] if ranking in cache_handler.other_search_term_dict else [],
        }})

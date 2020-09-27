"""
Called by app.py when `/error` route is called.

Last updated: MB 27/09/2020 - created module.
"""
# import external libraries.
import os
from flask import render_template, request

# import local modules.
from src import error_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve new bot information from DynamoDB if 'refresh'
    parameter is True. Otherwise use the currently cached bot data.
    """
    @app.route("/errors", methods=['GET'])
    def errorDashboard():
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload bot information into the cache.
        if refresh is True:
            print('refresh error list...')
            error_controller.update_error_cache()

        # render the bot template with current cached data.
        return render_template('pages/errorDashboard.html', data={**cache_handler.render_dict, **{
            'errors': cache_handler.error_dict,
        }})

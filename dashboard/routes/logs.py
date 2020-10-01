"""
Called by app.py when `/log` route is called.

Last updated: MB 27/09/2020 - created module.
"""
# import external libraries.
import os
from flask import render_template, request, jsonify, redirect

# import local modules.
from src import log_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve new error information from DynamoDB if 'refresh'
    parameter is True. Otherwise display the currently cached error data.
    """
    @app.route("/logs", methods=['GET'])
    def logDashboard():
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload bot information into the cache.
        if refresh is True:
            print('refresh log list...')
            log_controller.update_log_cache()

        # render the log template with current cached data.
        return render_template('pages/logDashboard.html', data={**cache_handler.render_dict, **{
            # order dictionary into a list and order by reverse run start time.
            'logs': reversed(sorted(cache_handler.log_dict.items(), key=lambda x: x[0])),
        }})

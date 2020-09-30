"""
Called by app.py when `/error` route is called.

Last updated: MB 27/09/2020 - created module.
"""
# import external libraries.
import os
from flask import render_template, request, jsonify, redirect

# import local modules.
from src import error_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve new error information from DynamoDB if 'refresh'
    parameter is True. Otherwise display the currently cached error data.
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

    """
    Called by app.py. delete the error from cache and the db project.
    """
    @app.route("/error/del", methods=['POST'])
    def deleteError():
        # retrieve all log file names.
        log_files = [v for v in request.form if '.log' in v]

        # if there was a not a log file 'name' in the form, return invalid.
        if len(log_files) == 0:
            return jsonify(status=400, success=False)

        # run delete function.
        error_controller.remove_error(log_files[0])

        # render the bot template with current cached data.
        return redirect("/errors")

"""
Called by app.py when `/ads` route is called.

Last updated: MB 9/09/2020 - copied template from 'bots' route.
"""
# import external libraries.
import os
from flask import render_template, jsonify, request

# import local modules.
from src import ad_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """"
    Called by app.py. Retrieve new ad information from DynamoDB if 'refresh'
    parameter is True. Otherwise use the currently cached ad data.
    """
    @app.route("/ads", methods=['GET'])
    def ads():
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload ad information into the cache.
        if refresh is True:
            print('refresh ads')
            ad_controller.update_ad_cache()

        # render the ad template with current cached data.
        return render_template('pages/adDashboard.html', data={**cache_handler.render_dict, **{
            'ads': cache_handler.ad_list,
            'bots': cache_handler.bot_dict,
        }})

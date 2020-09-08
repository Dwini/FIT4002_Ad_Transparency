"""
Called by app.py when `/ads` route is called.

Last updated: MB 9/09/2020 - copied template from 'bots' route.
"""
# import external libraries.
import os
from flask import render_template, request, redirect

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
    def adDashboard():
        # check for refresh argument.
        refresh = request.args.get('refresh', default=False, type=bool)

        # if refresh is true, reload ad information into the cache.
        if refresh is True:
            print('refresh ads')
            ad_controller.update_ad_cache()

        # render the ad template with current cached data.
        return render_template('pages/adDashboard.html', data={**cache_handler.render_dict, **{
            'ads': cache_handler.ad_dict,
            'bots': cache_handler.bot_dict,
        }})

    """"
    Called by app.py. display more information about this advertisement and the
    bot that scraped it.
    id: string referring to the id of the advertisement.
    """
    @app.route("/ad/<string:id>", methods=['GET'])
    def ad(id):
        # if this ad does not exit, return to ad dashboard.
        if id not in cache_handler.ad_dict:
            return redirect('/ads', code=302)

        # get this ad.
        ad = cache_handler.ad_dict[id]

        # get the bot that saved this ad. if there was no bot, ad placeholder
        # information.
        bot = cache_handler.bot_dict[ad['bot']] if ad['bot'] in cache_handler.bot_dict else {
            'password': '-',
            'dob': '-',
            'gender': '-',
            'political_ranking': '-',
            'name': '-',
            'latitude': '-',
            'longitude': '-',
        }

        # render the ad template with current cached data.
        return render_template('pages/ad.html', data={**cache_handler.render_dict, **{
            'id': id,
            'ad': ad,
            'bot': bot,
        }})

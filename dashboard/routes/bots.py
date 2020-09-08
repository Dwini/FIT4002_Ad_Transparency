"""
Called by app.py when `/bots` route is called.

Last updated: MB 9/09/2020 - created module from boilerplate flask code.
"""
# import external libraries.
import os
from flask import render_template

# import local modules.
from src import bot_controller, cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve bot information from DynamoDB.
    """
    @app.route("/bots", methods=['GET'])
    def bots():
        # render the index template.
        return render_template('pages/bots.html', data={**cache_handler.render_dict, **{
            'bots': bot_controller.get_bot_list(),
        }})

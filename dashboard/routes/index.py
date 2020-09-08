"""
Called by app.py when `/bots` route is called.

Last updated: MB 9/09/2020 - created module from boilerplate flask code.
"""
# import external libraries.
import os
from flask import abort, request, render_template

# import local modules.
from src import cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Retrieve bot information from DynamoDB.
    """
    @app.route("/", methods=['GET'])
    def index():
        # render the index template.
        return render_template('pages/index.html', data=cache_handler.render_dict)

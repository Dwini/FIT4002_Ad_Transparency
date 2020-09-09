"""
Called by app.py when `/bots` route is called.

Last updated: MB 9/09/2020 - created module from boilerplate flask code.
"""
# import external libraries.
from flask import render_template

# import local modules.
from src import cache_handler

"""
Called in app.py to initialise the routes in this file.
"""
def init(app):

    """
    Called by app.py. Render basic dashboard.
    """
    @app.route("/", methods=['GET'])
    def index():
        # render the index template.
        return render_template('pages/index.html', data=cache_handler.render_dict)

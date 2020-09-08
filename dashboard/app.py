"""
This is the main application for the Ad Transparency Dashboard project. It will
link routes files and provide an entrypoint for gunicorn.

Last updated: MB 8/09/2020 - copied boilerplate flask code.
"""
# import external libraries.
import os, sys, json
from flask import Flask, request, abort

# import routes.
import routes.index

# define constants.
FILENAME = os.path.basename(__file__)

# define app.
app = Flask(__name__, template_folder='public/templates', static_folder='public/static')

# initialise routes.
routes.index.init(app)

# called on startup.
if __name__ == "__main__":
    # retrieve hostname and port from arguments.
    args = sys.argv

    # start the GEM server in a dedicated process.
    host = args[1] if len(args)>2 else '0.0.0.0'
    port = args[2] if len(args)>3 else int(os.environ.get('PORT', 5000))
    app.run(host = host, port = port)

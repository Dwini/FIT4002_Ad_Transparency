"""
This module handles the cached global values for the Ad Transparency
dashboard project.

Last updated: MB 30/09/2020 - add db_uri to cache.
"""
# import external libraries.
import pytz, os, dotenv
from datetime import datetime
dotenv.load_dotenv()

"""
Set the address of the db endpoint.
"""
db_uri = os.getenv('DB_URI') or 'http://localhost:8080'  # default db project endpoint.

"""
This dictionary is sent to each web page. To add additional data to the webpage,
merge another dictionary with this one using the following notation:
    `data={**cache_handler.render_dict, **dict2}`
"""
render_dict = {
    'build_time': datetime.now(tz=pytz.timezone('Australia/Melbourne')),
}

"""
This is a dictionary with the username of the bot as a key, and an object
containing the bots attributes.
username = {
    password: str,
    dbo: str,
    gender: str,
    political_ranking: int,
    name: str,
    latitude: float,
    longitude: float,
}
"""
bot_dict = dict()

"""
This is a dictionary with the id of the advertisement as a key, and an object
containing the ads attributes.
id = {
    bot: str (username of bot),
    link: str,
    file: str,
    datetime: datetime,
}
"""
ad_dict = dict()

"""
This is a dictionary with the id of the political ranking as a key, and a list
of political search terms as the value.
"""
political_search_term_dict = dict()

"""
This is a dictionary with the id of the other ranking as a key, and a list
of other search terms as the value.
"""
other_search_term_dict = dict()

"""
This is a dictionary with the id of the error entry as a key, and a dictionary
of error attributes as the value.
"""
error_dict = dict()

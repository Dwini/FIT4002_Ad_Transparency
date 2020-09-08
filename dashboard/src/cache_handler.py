"""
This module handles the cached global values for the Ad Transparency
dashboard project.

Last updated: MB 8/09/2020 - copy boilerplate code from previous flask project.
"""
# import external libraries.
import pytz, signal
from datetime import datetime

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
This holds a list of advertisement objects.
ad = {
    bot: str (username of bot),
    link: str,
    file: str,
    datetime: datetime,
    id: str,
}
"""
ad_list = []

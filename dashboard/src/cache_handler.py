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
    `data={**cache_handler.render_dict, **dict2} `
"""
render_dict = {
    'build_time': datetime.now(tz=pytz.timezone('Australia/Melbourne')),
}

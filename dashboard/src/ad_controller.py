"""
This module handles the downloading and parsing of ad information from the
DynamoDB. This information is in a structured format to be rendered in HTML.

Last updated: MB 8/09/2020 - copied module from 'bot_controller' as a template.
"""
# import local modules.
from src import db_controller, cache_handler

"""
This function will update the cached ad list. Each element in the list is an
object holding advertisement information.
"""
def update_ad_cache():
    # clear the currently cached list of ads.
    cache_handler.ad_dict.clear()

    # retrieve all raw data from 'Ads' table in AWS DynamoDB.
    raw_data = db_controller.get_full_table('Ads')

    # iterate over each item in the raw data and append the information to the
    # the ad_dict.
    for item in raw_data['Items']:
        # parse data and add to ad_dict. set id as the key and create an
        # object as the value.
        cache_handler.ad_dict[item['id']['S']] = {
            'bot': item['bot']['S'] if 'bot' in item else '-',
            'datetime': item['datetime']['S'] if 'datetime' in item else '-',
            'file': item['file']['S'] if 'file' in item else '-',
            'link': item['link']['S'] if 'link' in item else '-',
        }

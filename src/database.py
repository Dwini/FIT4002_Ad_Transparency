import boto3
import uuid
import random
from time import sleep
from datetime import datetime

from config import keys, constants

def Ad(bot_id, link, headline, html_string):
    date_captured = datetime.now().strftime(constants.datetime_format)
    return {
        'id': str(uuid.uuid4()),
        'date_captured': date_captured,
        'bot_id': bot_id,
        'link': link,
        'headline': headline,
        'html_string': html_string
    }

def Log(bot_id, url, actions, search_term):
    date_logged = datetime.now().strftime(constants.datetime_format)
    return {
        'id': str(uuid.uuid4()),
        'date_logged': date_logged,
        'bot_id': bot_id,
        'url': url,
        'actions': actions,
        'search_term': search_term
    }


class Database:

    def __init__(self):
        # connect to database
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
            region_name=keys.REGION_NAME
        )
        self.ads = dynamodb.Table('Ads')
        self.bots = dynamodb.Table('Bots')
        self.logs = dynamodb.Table('Logs')

    def get_all_bots(self):
        # return a list of all bots in db
        print("Fetching all bots...", end="")
        response = self.bots.scan()['Items']

        print("success\n%d bots fetched" % (len(response)))
        return response

    def log_action(self, bot_id, url, actions, search_term='<n/a>'):
        actions = ', '.join(actions)

        print("Logging %s at %s ... " % (actions, url), end="")
        self.logs.put_item(
            Item=Log(
                bot_id=bot_id,
                url=url,
                actions=actions,
                search_term=search_term
            )
        )
        print("success")

    def save_ad(self, bot_id, link, headline, html_string):
        print("Saving ad with link %s ... " % (link), end='')
        self.ads.put_item(
            Item=Ad(
                bot_id=bot_id,
                link=link,
                headline=headline,
                html_string=html_string
            )
        )
        print("success")

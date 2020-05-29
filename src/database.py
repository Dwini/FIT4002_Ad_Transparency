import boto3
import uuid
import random
import csv
from datetime import datetime

from config import keys, constants

class Database:
    def __init__(self):
        # connect to database
        print('connecting to database...', end="")
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
            region_name=keys.REGION_NAME
        )
        print("success")

        # init tables
        self.ads =  dynamodb.Table('Ads')
        self.bots = dynamodb.Table('Bots')
        self.logs = dynamodb.Table('Logs')

    """
    Return all the items in a table given the table name
    """
    def fetch_all_items(self, table_name):
        print("fetching items from %s table..." % table_name, end="")

        if table_name == 'Ads':
            response = self.ads.scan()['Items']
        elif table_name == 'Bots':
            response = self.bots.scan()['Items']
        elif table_name == 'Logs':
            response = self.logs.scan()['Items']

        print("success (%d items fetched)" % (len(response)))
        return response

    """
    Create a bot given the bots info
    """
    def create_bot(self, username, password, date_created, name, gender, DOB, search_terms):
        print("creating bot %s..." % (username), end="")
        self.bots.put_item(Item={
            'username': username,
            'password': password,
            'date_created': date_created,
            'name': name,
            'gender': gender,
            'DOB': DOB,
            'search_terms': search_terms
        })
        print("success")

    """
    Logs a bots actions on a page. If bot was searching then include
    the search term
    """
    def log_action(self, bot_username, url, actions, search_term=''):
        date_logged = datetime.now().strftime(constants.datetime_format)

        print("logging %s at '%s'..." % (actions, url), end="")
        self.logs.put_item(Item={
            'id': str(uuid.uuid4()),
            'date_logged': date_logged,
            'bot_username': bot_username,
            'url': url,
            'actions': actions,
            'search_term': search_term
        })
        print("success")

    """
    Save an ad to the database. Currently just saves the html of the ad
    """
    def save_ad(self, bot_username, link, headline, html_string):
        date_captured = datetime.now().strftime(constants.datetime_format)

        print("saving ad with link %s..." % (link), end='')
        self.ads.put_item(Item={
            'id': str(uuid.uuid4()),
            'date_captured': date_captured,
            'bot_username': bot_username,
            'link': link,
            'headline': headline,
            'html_string': html_string
        })
        print("success")


"""
Export info for a particular table to csv file
"""
def export_to_csv(table_name, items):
    if len(items) == 0:
        print("no items in %s table" % table_name)
        return

    # get all atrribute names 
    # (doesn't preserver proper ordering though)
    fieldnames = set().union(*items)

    filename = '%s.csv' % table_name.lower()

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for item in items:
            writer.writerow(item)

    print("exported to %s" % filename)


if __name__ == '__main__':
    db = Database()

    choice = int(input(           \
        "(1) Export Bots\n"     + \
        "(2) Export Ads\n"      + \
        "(3) Export Logs\n"     + \
        "(4) Create bot\n"      + \
        "Enter number (1-4)> "    \
    ))
    
    if choice == 1:
        items = db.fetch_all_items('Bots')
        export_to_csv('Bots', items)
    elif choice == 2:
        items = db.fetch_all_items('Ads')
        export_to_csv('Ads', items)
    elif choice == 3:
        items = db.fetch_all_items('Logs')
        export_to_csv('Logs', items)
    elif choice == 4:
        username =      input("Enter username> ")
        password =      input("Enter password> ")
        date_created =  input("Enter date this bot was created (format dd-MM-YYYY)> ")
        name =          input("Enter name (seperated by ', ')> ").split(", ")
        gender =        input("Enter gender> ")
        DOB =           input("Enter DOB (format dd-MM-YYYY)> ")
        search_terms =  input("Enter search_terms (seperated by ', ')> ").split(", ")

        db.create_bot(
            username=username,
            password=password,
            date_created=date_created,
            name=name,
            gender=gender,
            DOB=DOB,
            search_terms=search_terms
        )
    else:
        print("Invalid option")
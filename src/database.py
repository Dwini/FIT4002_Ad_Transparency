import boto3
import uuid
import random
import csv
from datetime import datetime

from config import keys, constants

FETCHING_TEXT = "Fetching items..."
SUCCESS_TEXT = "success (%d items fetched)"

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

    def fetch_all_items(self, table_name):
        # return all entries in a table
        print(FETCHING_TEXT, end="")

        if table_name == 'Ads':
            response = self.ads.scan()['Items']
        elif table_name == 'Bots':
            response = self.bots.scan()['Items']
        elif table_name == 'Logs':
            response = self.logs.scan()['Items']

        print(SUCCESS_TEXT % (len(response)))
        return response

    def create_bot(self, username, password, date_created, name, gender, DOB, search_terms):
        print("Creating bot with username %s ... " % (username), end="")
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

    def log_action(self, bot_username, url, actions, search_term=''):
        date_logged = datetime.now().strftime(constants.datetime_format)

        print("Logging %s at %s ... " % (actions, url), end="")
        self.logs.put_item(Item={
            'id': str(uuid.uuid4()),
            'date_logged': date_logged,
            'bot_username': bot_username,
            'url': url,
            'actions': actions,
            'search_term': search_term
        })
        print("success")

    def save_ad(self, bot_username, link, headline, html_string):
        date_captured = datetime.now().strftime(constants.datetime_format)

        print("Saving ad with link %s ... " % (link), end='')
        self.ads.put_item(Item={
            'id': str(uuid.uuid4()),
            'date_captured': date_captured,
            'bot_username': bot_username,
            'link': link,
            'headline': headline,
            'html_string': html_string
        })
        print("success")

def export_to_csv(table_name, items, fieldnames):
        if len(items) == 0:
            print("No items in %s table" % table_name)
            return

        # programmatically get all atrribute names 
        # (doesn't preserver proper ordering though)
        #
        # fieldnames = set().union(*items)

        filename = '%s.csv' % table_name.lower()

        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item)

        print("Exported to %s" % filename)


def main():
    db = Database()

    choice = int(input(         \
        "(1) Export Bots\n"   + \
        "(2) Export Ads\n"    + \
        "(3) Export Logs\n"   + \
        "(4) Create bot\n"   + \
        "Enter number (1-4)>"   \
    ))

    if 1 <= choice <= 3:
        if choice == 1:
            table_name = 'Bots'
            fieldnames = [ 
                "username",
                "password",
                "date_created",
                "name",
                "gender",
                "DOB",
                "search_terms" 
            ]
        elif choice == 2:
            table_name = 'Ads'
            fieldnames = [ 
                'id',
                'date_captured',
                'bot_username',
                'link',
                'headline',
                'html_string'
            ]
        elif choice == 3:
            table_name = 'Logs'
            fieldnames = [ 
                'id',
                'date_logged',
                'bot_username',
                'url',
                'actions',
                'search_term'
            ]

        items = db.fetch_all_items(table_name)
        export_to_csv(table_name, items, fieldnames)

    elif choice == 4:
        username=input("Enter username>")
        password=input("Enter password>")

        date_created = input("Enter date this bot was created (format dd-MM-YYYY)>")

        name=input("Enter name (seperated by ', ')>").split(", ")
        gender=input("Enter gender>")
        DOB=input("Enter DOB (format dd-MM-YYYY)>")
        search_terms=input("Enter search_terms (seperated by ', ')>").split(", ")

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

if __name__ == '__main__':
    main()

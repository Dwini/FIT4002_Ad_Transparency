import boto3
import uuid
import random
import csv
from datetime import datetime

from config import keys, constants

class Database:
    def __init__(self):
        print('connecting to DynamoDB...', end="")
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
            region_name=keys.REGION_NAME
        )
        print("success")

        print('connecting to S3...', end="")
        s3 = boto3.resource(
            's3',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY
        )
        print("success")

        # init tables
        self.ads =  dynamodb.Table('Ads')
        self.bots = dynamodb.Table('Bots')
        self.logs = dynamodb.Table('Logs')

        # init bucket
        self.bucket = s3.Bucket(keys.BUCKET_NAME)

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

    def fetch_all_objects(self):
        """
        Get all the objects currently stored in the S3 bucket
        """
        return self.bucket.objects.all()

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

    def save_ad(self, bot_username, link, headline, html_string, file_id=''):
        """
        Save an ad to the database along with any relevant metadata.

        :param bot_username:    Username of the bot that logged this ad
        :param link:            URL of the ad
        :param headline:        Title/Headline of ad
        :param html_string:     The HTML of the ad
        :param file_id:         ID of file that was uploaded to S3 
            related to this ad
        """
        date_captured = datetime.now().strftime(constants.datetime_format)

        print("saving ad with link %s..." % (link), end='')
        self.ads.put_item(Item={
            'id': str(uuid.uuid4()),
            'date_captured': date_captured,
            'bot_username': bot_username,
            'link': link,
            'headline': headline,
            'html_string': html_string,
            'file_id': file_id
        })
        print("success")

    def upload_file(self, path):
        """
        Save a file to S3.

        :param path: Path to the file as a string. Path is relative
            so for example if filename is 123.jpg under the adScreenshots
            directory then path = 'adScreenshots/123.jpg'
        :return: ID of the uploaded S3 file. This can then be used when
            logging an ad to link the uploaded file to the new ad
        """
        date = datetime.now().strftime(constants.datetime_format)
        id = str(uuid.uuid4())

        print('uploading file to s3...', end='')
        try:
            self.bucket.upload_file(path, id)
            print('done')
            return id
        except Exception as e:
            print('\nError: %s' % str(e))
            return None

def export_to_csv(table_name, items):
    """
    Export info for a particular table to csv file
    """
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

def main():
    db = Database()

    choice = int(input(                   \
        "(1) Export Bots\n"             + \
        "(2) Export Ads\n"              + \
        "(3) Export Logs\n"             + \
        "(4) Create Bot\n"              + \
        "(5) List bucket objects\n"     + \
        "Enter number (1-5)> "            \
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
    elif choice == 5:
        total_size = 0
        for o in db.fetch_all_objects():
            print('%s\t%s\t%s bytes' % (o.key, o.last_modified, o.size))
            total_size += o.size
        print('Total size of all objects: %s bytes' % total_size)
    else:
        print("Invalid option")
    
    print("Exiting...")

if __name__ == '__main__':
    main()
import boto3
import uuid
import random
import csv
import os
from datetime import datetime

from config import keys, constants

def create_valid_dict(old_dict, required, optional):
    """
    Creates a new dictionary from a given dictionary
    removing unnecessary fields.
    
    :param old_dict:    (dict) Dictionary to prune
    :param required:    (array of strings) Defines the required
        fields. If any of these fields are not found in old_dict,
        an error will be raised
    :param optional     (array of strings) List of allowed optional
        fields that can be kept from old_dict
    :return new_dict:   (dict) New dictionary with required and optional
        fields only
    """
    try:
        # Check all required values exist
        new_dict = { k: old_dict[k] for k in required }
    except:
        raise KeyError("Missing required value(s)")

    for k in optional:
        if k in old_dict:
            new_dict[k] = old_dict[k]
    
    return new_dict

class Database:
    def __init__(self):
        print('>> Connecting to DynamoDB...', end="")
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
            region_name=keys.REGION_NAME
        )
        print("done")

        print('>> Connecting to S3...', end="")
        s3 = boto3.resource(
            's3',
            aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY
        )
        print("done")

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
        print(">> Fetching %s..." % table_name, end="")

        if table_name == 'Ads':
            response = self.ads.scan()['Items']
        elif table_name == 'Bots':
            response = self.bots.scan()['Items']
        elif table_name == 'Logs':
            response = self.logs.scan()['Items']

        print("done (%d items fetched)" % (len(response)))
        return response

    def fetch_all_objects(self):
        """ Get all the objects currently stored in the S3 bucket """
        items = self.bucket.objects.all()
        print(">> %d objects in bucket" % len(list(items)))
        return items

    # TODO: Remove this. Tedious when creating bots here.
    def create_bot(self, bot):
        """
        Creates a new bot

        :param action: Dictionary that contains the following keys:
            - username:     (string) Username of bot
            - password:     (string) Password to bots account
            - date_created: (string) Date bot was created
            - name:         (array of string) Name of bot
            - gender:       (string) Gender of bot
            - DOB:          (string) Date of birth of bot
            - search_terms  (array of strings) Terms the bot will use to search
        """
        print(">> Creating bot: %s ..." % bot["username"], end="")
        self.bots.put_item(Item=bot)
        print("done")

    def log_action(self, action):
        """
        Logs a bots actions on a page. If bot was searching then include
        the search term

        :param action: Dictionary that contains the following keys:
            - bot:          (string) Username of the bot that logged this action
            - url:          (string) Url that the action was logged at
            - actions:      (array of strings) Actions that were performed, e.g. 'search', 'visit'
            - search_term:  (string, optional) if search was performed the terms that 
                            were queried
        """
        required_fields = ["bot", "url", "actions"]
        optional_fields = ["search_term"]
        new_action = create_valid_dict(action, required_fields, optional_fields)

        new_action["id"] = str(uuid.uuid4())
        new_action["datetime"] = datetime.now().strftime(constants.datetime_format)

        print(">> Logging %s at '%s' ..." % (new_action["actions"], new_action["url"]), end="")
        self.logs.put_item(Item=new_action)
        print("done")

    def save_ad(self, ad):
        """
        Save an ad to the database along with any relevant metadata.

        :param ad: Dictionary that contains the following keys:
            - bot:          (string) Username of the bot that logged this ad
            - link:         (string) URL of the ad
            - headline:     (string) Title/Headline of ad
            - html:         (string) The HTML of the ad
            - file_id:      (string, optional) ID of file that was uploaded to S3 
                related to this ad. This is given when uploading files (see 
                upload_file below)
            - base64        (string, optional) Base64 string of ad
        """
        required_fields = ["bot", "link", "headline", "html"]
        optional_fields = ["file_id", "base64"]
        new_ad = create_valid_dict(ad, required_fields, optional_fields)
            
        new_ad["id"] = str(uuid.uuid4())
        new_ad["datetime"] = datetime.now().strftime(constants.datetime_format)

        print(">> Saving ad: %s ..." % (new_ad["headline"]), end="")
        self.ads.put_item(Item=new_ad)
        print("done")

    def upload_file(self, path):
        """
        Save a file to S3.

        :param path: Path to the file as a string. Path is relative
            so for example if filename is 123.jpg under the adScreenshots
            directory then path = 'adScreenshots/123.jpg'
        :return: ID of the uploaded S3 file. This can then be used when
            logging an ad to link the uploaded file to the new ad
        """
        file_id = str(uuid.uuid4())

        print('>> Uploading file to S3...', end="")
        self.bucket.upload_file(path, file_id)
        print("done")

        return file_id

def export_table(db, table_name):
    """
    Export info for a particular table to csv file
    """
    items = db.fetch_all_items(table_name)
    if len(items) == 0:
        print(">> %s table is empty, no file will be created" % table_name)
        return

    fieldnames = set().union(*items)    # Get all atrribute names
    filename = 'tmp/%s.csv' % table_name.lower()

    with open(filename, 'w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def export_bucket(db):
    items = db.fetch_all_objects()

    if len(list(items)) == 0:
        print(">> Bucket is empty, no file will be created")
        return

    total_size = 0   
    filename = 'tmp/files.csv'

    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ "key", "datetime", "size (bytes)" ])
        for i in items:
            writer.writerow([i.key, i.last_modified, i.size])
            total_size += i.size
        writer.writerow([ "", "Total", "%s" % total_size ])

def main():
    db = Database()

    choice = int(input("\n"               \
        "(1) Export all data\n"         + \
        "(2) Create Bot\n"              + \
        ">> Enter number> "               \
    ))
    print("")
    
    if choice == 1:
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        export_table(db, 'Bots')
        export_table(db, 'Ads')
        export_table(db, 'Logs')
        export_bucket(db)
        print(">> Export complete. All files saved to 'tmp' folder")
    elif choice == 2:
        bot = {}
        bot["username"] =      input("Enter username> ")
        bot["password"] =      input("Enter password> ")
        bot["date_created"] =  input("Enter date this bot was created (format dd-MM-YYYY)> ")
        bot["name"] =          input("Enter name (seperated by ', ')> ").split(", ")
        bot["gender"] =        input("Enter gender> ")
        bot["DOB"] =           input("Enter DOB (format dd-MM-YYYY)> ")
        bot["search_terms"] =  input("Enter search_terms (seperated by ', ')> ").split(", ")
        db.create_bot(bot)
    else:
        print(">> Error: Invalid option")

if __name__ == '__main__':
    main()
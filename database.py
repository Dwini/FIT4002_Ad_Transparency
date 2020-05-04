import boto3
from time import sleep
from datetime import datetime

import config.keys as keys
from models.Ad import Ad
from models.Bot import Bot
from models.Log import Log

# connect to database
client = boto3.client(
    'dynamodb', 
    aws_access_key_id=keys.aws_access_key_id, 
    aws_secret_access_key=keys.aws_secret_access_key,
    region_name='us-east-2'
)

# create bot using model
new_bot = Bot(
    name=['John', 'Smith'],
    username='johnsmith',
    password='password123',
    sex='M',
    DOB=datetime(1990, 4, 3)
)
bot_id = new_bot['id']['S']

# save bot to db
print('Creating new bot...')
response = client.put_item(
    TableName='Bots',
    Item=new_bot
)

# get bot from db
response = client.get_item(
    TableName='Bots',
    Key={ 'id': { 'S': bot_id } }
)['Item']
print('%s\n' % response)

# log that bot visited Google
print('Logging that bot visitied Google...')
response = client.put_item(
    TableName='Logs',
    Item=Log(
        bot_id=bot_id,
        url='https://google.com',
        actions=['visit', 'search'],
        search_term='donald trump'
    )
)

# list log entries of bot
print('Finding log entries of bot...')
response = client.scan(
    TableName='Logs',
    FilterExpression="bot_id = :b",
    ExpressionAttributeValues={ ':b': { 'S': bot_id } }
)['Items']
print(response, end="\n\n")

# create ad for new bot
print('Saving ad bot collected to database...')
client.put_item(
    TableName='Ads',
    Item=Ad(
        bot_id=bot_id,
        url="https://google.com",
        html_string="some content"
    )
)

# find all ads collected by bot
print('Finding ads collected by bot...')
response = client.scan(
    TableName='Ads',
    FilterExpression="bot_id = :b",
    ExpressionAttributeValues={ ':b': { 'S': bot_id } }
)['Items']
print(response)
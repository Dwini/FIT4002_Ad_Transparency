import boto3
import uuid

from time import sleep
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb', 
    aws_access_key_id='AKIAWOMH53B2DNIVRXEQ', 
    aws_secret_access_key='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',
    region_name='us-east-2'
)

table = dynamodb.Table('Ads')

# create random id
id = str(uuid.uuid4())

# create an item to store
table.put_item(
    Item={
        'id': id,
        'html_string': '<p>Test ad</p>',
        'captured_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
)

# retrieve item
response = table.get_item(
    Key={
        'id': id
    }
)
print("Created new document:\n%s\n" % response['Item'])

# update item
table.update_item(
    Key={
        'id': id
    },
    UpdateExpression="set captured_on = :d",
    ExpressionAttributeValues={
        ':d': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    ReturnValues="UPDATED_NEW"
)
response = table.get_item(
    Key={
        'id': id
    }
)
print("Updated document:\n%s\n" % response['Item'])

# delete item
response = table.delete_item(
    Key={
        'id': id
    }
)
"""
This module handles the retrieval of data from the dynamodb instance on AWS.
Each function retrieves raw data which will be parsed by specific modules.

Last updated: MB 8/09/2020 created module from tutorial https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html.
"""
# import external libraries.
import os, dotenv, boto3
dotenv.load_dotenv()

# setup the DB client from environment variables.
dynamo_client = boto3.client('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), \
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name=os.getenv('AWS_REGION'))

"""
Return a full dump of the table specified as input. This will need to be parsed.
Table name: str ('Bots', 'Ads').
"""
def get_full_table(table_name):
    return dynamo_client.scan(TableName=table_name)

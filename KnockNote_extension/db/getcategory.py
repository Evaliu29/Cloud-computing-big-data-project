import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    print(event)
    print(context)
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Category')

    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'userid': {
                'AttributeValueList': [userid],
                'ComparisonOperator': 'EQ'
            }
        })
    res = []
    for entry in check["Items"]:
        res.append(entry["categoryname"])

    return {
        'statusCode': 200,
        'body': res
    }

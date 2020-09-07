import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Category')
    cate_name = event["name"]
    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'userid': {
                'AttributeValueList': [userid],
                'ComparisonOperator': 'EQ'
            }
        })

    for entry in check["Items"]:
        if entry["categoryname"] == cate_name:
            return {
                'statusCode': 200,
                'body': {
                    "success": "false",
                    "content": " You have already have this category"

                }
            }

    timestamp = int(time.time())
    categoryid = str(timestamp)
    dynamo_info = {
        "categoryid": categoryid,
        "userid": userid,
        "categoryname": cate_name
    }

    dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    response = table.put_item(Item=dynamo_data)
    success = True
    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": " Successfully creat the category!"

        }
    }

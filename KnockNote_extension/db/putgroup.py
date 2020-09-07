import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Group')
    group_name = event["groupname"]
    userid = event["userid"]
    describ = event["description"]
    user = [userid]
    timestamp = int(time.time())
    groupid = str(timestamp)
    dynamo_info = {
        "groupid": groupid,
        "groupname": group_name,
        "userid": user,
        "description": describ
    }

    dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    response = table.put_item(Item=dynamo_data)
    success = True
    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": " Successfully creat the group!"

        }
    }

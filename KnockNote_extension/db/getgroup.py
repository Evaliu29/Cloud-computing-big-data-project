import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Group')

    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'userid': {
                'AttributeValueList': [userid],
                'ComparisonOperator': 'CONTAINS'
            }
        })
    res = []
    for entry in check["Items"]:
        temp = {}
        temp["groupname"] = entry["groupname"]
        temp["groupid"] = entry["groupid"]
        temp["userid"] = entry["userid"]
        temp["description"] = entry["description"]
        res.append(temp)

    return {
        'statusCode': 200,
        'body': res,
        # "test":json.dumps(check)
    }

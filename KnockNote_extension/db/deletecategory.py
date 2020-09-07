import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Category')
    table2 = dynamodb.Table('Note')
    cate_name = event["name"]
    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'userid': {
                'AttributeValueList': [userid],
                'ComparisonOperator': 'EQ'
            },
            'categoryname': {
                'AttributeValueList': [cate_name],
                'ComparisonOperator': 'EQ'
            }

        })
    check2 = table2.scan(
        ScanFilter={
            'category': {
                'AttributeValueList': [cate_name],
                'ComparisonOperator': 'EQ'
            }

        })

    categoryid = None
    success = False
    if len(check["Items"]) > 0:
        categoryid = check["Items"][0]["categoryid"]

    if categoryid is not None:
        response = table.delete_item(
            Key={
                'categoryid': categoryid
            }
        )

        success = True
        content = "Successfully deleted!"
    else:
        content = "No such info"

    if len(check2["Items"]) > 0:
        for entry in check2["Items"]:
            table2.update_item(

                Key={'noteid': entry["noteid"]},
                UpdateExpression="set category =:i",
                ExpressionAttributeValues={":i": "null"},
                ReturnValues="UPDATED_NEW"
            )

        success = True
        content = "Successfully deleted!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content
        }
    }

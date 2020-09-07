import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Group')
    group_id = event["groupid"]
    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'groupid': {
                'AttributeValueList': [group_id],
                'ComparisonOperator': 'EQ'
            }
        })
    success = True
    content = "Successfully delet the group"
    if len(check["Items"]) > 0:

        userlist = check["Items"][0]["userid"]
        if userlist is not None and userid == userlist[0]:
            response = table.delete_item(
                Key={
                    'groupid': group_id
                }
            )
            table2 = dynamodb.Table('GroupMessage')
            check2 = table2.scan(
                ScanFilter={
                    'groupid': {
                        'AttributeValueList': [group_id],
                        'ComparisonOperator': 'EQ'
                    }
                })
            if len(check2["Items"]) > 0:
                for entry in check2["Items"]:
                    response = table2.delete_item(
                        Key={
                            'groupmessageid': entry['groupmessageid']
                        }
                    )



        else:
            content = "You have no right to delet"
            success = False
    else:
        content = "No such Gro"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content

        }
    }
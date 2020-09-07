import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Group')

    groupid = event["groupid"]
    userid = event["userid"]
    check = table.scan(
        ScanFilter={
            'groupid': {
                'AttributeValueList': [groupid],
                'ComparisonOperator': 'EQ'
            }
        })
    success = True
    content = " Joined successfull"
    if len(check["Items"]) > 0:
        userlist = check["Items"][0]["userid"]
        if userid not in userlist:
            userlist.append(userid)
            table.update_item(

                Key={'groupid': check["Items"][0]["groupid"]},
                UpdateExpression="set userid =:i",
                ExpressionAttributeValues={":i": userlist},
                ReturnValues="UPDATED_NEW"
            )

        else:
            success = False
            content = "Already in the list"

    else:
        content = "No such Group"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content

        }

    }

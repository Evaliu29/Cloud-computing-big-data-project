import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


# 接收 userid，message，groupid，生成groupMessageid，
# 生成时间，根据userid找对应username，添加groupmessage

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    groupMessage_table = dynamodb.Table('GroupMessage')
    group_id = event["groupid"]
    user_id = event["userid"]
    message = event["message"]
    messagetime = int(time.time())
    groupMessageid = str(int(time.time()))
    ##search for username from user table
    user_table = dynamodb.Table('User')
    match = user_table.query(
        KeyConditionExpression=Key('userid').eq(user_id)
    )
    user_name = match["Items"][0]["username"]
    dynamo_info = {
        "groupmessageid": groupMessageid,
        "userid": user_id,
        "groupid": group_id,
        "message": message,
        "messagetime": messagetime,
        "username": user_name
    }
    json.dumps(dynamo_info)
    dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    response = groupMessage_table.put_item(Item=dynamo_data)
    success = True
    content = "Message added successfully!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "messagetime": messagetime,
            "content": content
        }
    }

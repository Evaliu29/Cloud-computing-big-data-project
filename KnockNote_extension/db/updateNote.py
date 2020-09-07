import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


##接收noteID和参数，判断参数（null则不更新），更新category 和 writecontent，返回ture or false
def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Note')
    timestamp = time.time()
    timeArray = time.localtime(timestamp)
    timestring = time.strftime("%Y-%m-%d", timeArray)
    t = int(timestamp)
    note_id = event["noteid"]
    category = event["category"]
    writecontent = event["writecontent"]
    table.update_item(
        Key={'noteid': note_id},
        UpdateExpression="set category =:i",
        ExpressionAttributeValues={":i": category},
        ReturnValues="UPDATED_NEW"
    )
    table.update_item(
        Key={'noteid': note_id},
        UpdateExpression="set modifytime =:i",
        ExpressionAttributeValues={":i": timestring},
        ReturnValues="UPDATED_NEW"
    )
    table.update_item(
        Key={'noteid': note_id},
        UpdateExpression="set modifytimestamp =:i",
        ExpressionAttributeValues={":i": t},
        ReturnValues="UPDATED_NEW"
    )
    table.update_item(
        Key={'noteid': note_id},
        UpdateExpression="set writecontent =:i",
        ExpressionAttributeValues={":i": writecontent},
        ReturnValues="UPDATED_NEW"
    )

    success = True
    content = "Successfully updated!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content

        }
    }

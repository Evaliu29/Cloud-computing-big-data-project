import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


##接收参数，生成noteid，time，category设为null，
##添加note，返回ture or false


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Note')
    timestamp = time.time()
    timeArray = time.localtime(timestamp)
    timestring = time.strftime("%Y-%m-%d", timeArray)
    t = int(timestamp)
    note_id = str(t)
    user_id = event["userid"]
    page = event["pageurl"]
    img = event["imgurl"]
    select_content = event["selectedcontent"]
    write_content = event["writecontent"]
    category = "null"
    dynamo_info = {
        "userid": user_id,
        "noteid": note_id,
        "pageurl": page,
        "imageurl": img,
        "selectedcontent": select_content,
        "writecontent": write_content,
        "category": category,
        "modifytime": timestring,
        "modifytimestamp": t
    }
    json.dumps(dynamo_info)
    dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    response = table.put_item(Item=dynamo_data)
    success = True
    content = "Successfully added!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content
        }
    }

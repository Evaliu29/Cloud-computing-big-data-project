import json
import boto3
from boto3.dynamodb.conditions import Key


# 接收groupid，返回groupid对应所有message
def lambda_handler(event, context):
    # TODO implement
    group_id = event["groupid"]
    lasttime = event["lasttime"]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('GroupMessage')
    match = table.scan(
        AttributesToGet=[
            'userid', 'message', 'messagetime', 'username'
        ],
        ScanFilter={
            'groupid': {
                'AttributeValueList': [group_id],
                'ComparisonOperator': 'EQ'
            }
        })
    messageList = match["Items"]
    messageList = sorted(messageList, key=lambda i: i['messagetime'], reverse=True)
    messageList.reverse()
    if lasttime != "null":
        comparetime = int(lasttime)
        if messageList[len(messageList) - 1]["messagetime"] <= comparetime:
            get_message = []
        else:
            for i in range(len(messageList)):
                if messageList[i]["messagetime"] > comparetime:
                    break
            get_message = messageList[i:]
    else:
        get_message = messageList

    return {
        'statusCode': 200,
        'body': get_message
    }
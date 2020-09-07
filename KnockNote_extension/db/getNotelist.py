# 接收userid和category，返回对应所有note（category为null时获取userid下所有的）
import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Note')
    userid = event["userid"]
    category = event["category"]
    if category != "null":
        check = table.scan(
            AttributesToGet=[
                'noteid', 'category', 'pageurl', 'imageurl', 'selectedcontent', 'writecontent', 'modifytime',
                'modifytimestamp'
            ],
            ScanFilter={
                'userid': {
                    'AttributeValueList': [userid],
                    'ComparisonOperator': 'EQ'
                },
                'category': {
                    'AttributeValueList': [category],
                    'ComparisonOperator': 'EQ'
                }
            })
        get_message = check["Items"]
        get_message = sorted(get_message, key=lambda i: i['modifytimestamp'], reverse=True)
    else:
        check = table.scan(
            AttributesToGet=[
                'noteid', 'category', 'pageurl', 'imageurl', 'selectedcontent', 'writecontent', 'modifytime',
                'modifytimestamp'
            ],
            ScanFilter={
                'userid': {
                    'AttributeValueList': [userid],
                    'ComparisonOperator': 'EQ'
                }
            })
        get_message = check["Items"]
        get_message = sorted(get_message, key=lambda i: i['modifytimestamp'], reverse=True)

    return {
        'statusCode': 200,
        'body': get_message
    }

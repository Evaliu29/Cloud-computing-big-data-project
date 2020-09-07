import json
import boto3
from boto3.dynamodb.conditions import Key


##接收note id，用noteid进行删除，返回ture or false

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Note')
    note_id = event["noteid"]
    check = table.scan(
        ScanFilter={
            'noteid': {
                'AttributeValueList': [note_id],
                'ComparisonOperator': 'EQ'
            }
        })
    shouldelete = check["Count"]
    success = False
    content = " "
    if shouldelete > 0:
        ##delete
        response = table.delete_item(
            Key={
                'noteid': note_id
            }
        )
        success = True
        content = "Successfully deleted!"
    else:
        content = "Sorry, delete error!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content
        }
    }

import json
import boto3
from boto3.dynamodb.conditions import Key


##接受email和user password，用email查找，
##获取password，和user password比较，相同则返回userid，不同则返回false

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb',region_name='us-east-2')
    table = dynamodb.Table('User')
    email = event["email"]
    password = event["password"]
    match = table.scan(
                ScanFilter={
                     'email': {
                    'AttributeValueList': [email],
                    'ComparisonOperator': 'EQ'
                     }
                })
    check = match["Items"]
    content = " "
    user_id = "null"
    success = False
    if len(check)>0:
        get_password = match["Items"][0]["password"]
        if password == get_password:
            success = True
            user_id =  match["Items"][0]["userid"]
            content = "Welcome to Note!"
        else:
            content = "Sorry, wrong email or password, please try again!"

    else:
        content = "Sorry, wrong email or password, please try again!"
    return {
        'statusCode': 200,
        'body':{
            "success": success,
            "userid": user_id,
            "content": content
        }
    }

import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time
import random

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


##得到Email,userverify db check otp.match-generate userid put all into userdb.不match, success=false


def lambda_handler(event, context):
    # TODO implement

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    user_table = dynamodb.Table('User')
    verify_table = dynamodb.Table('UserVerify')
    user_id = " "
    user_name = event["username"]
    user_password = event["password"]
    email = event["email"]
    otp = event["verification"]

    ##search from db to find if there is matched email
    check = verify_table.scan(
        ScanFilter={
            'Verification': {
                'AttributeValueList': [otp],
                'ComparisonOperator': 'EQ'
            }
        })
    shouldinsert = check["Count"]
    success = False
    content = "Registered Successfully!"
    # delete in verifydb
    if shouldinsert > 0:
        ##delete in verify db
        response = verify_table.delete_item(
            Key={
                'email': email
            }
        )
        # insert in userdb
        timestamp = int(time.time())
        user_id = str(timestamp)
        dynamo_info = {
            "userid": user_id,
            "username": user_name,
            "password": user_password,
            "email": email
        }
        json.dumps(dynamo_info)
        dynamo_data = {key: value for key, value in dynamo_info.items() if value}
        response = user_table.put_item(Item=dynamo_data)
        content = "Registered Successfully!"
        success = True
    else:
        content = "Verification or registered failed. Please try again!"

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "userid": user_id,
            "content": content

        }
    }

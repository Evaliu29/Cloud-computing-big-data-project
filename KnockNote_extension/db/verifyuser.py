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


# input email, check email,generate otp, 发邮件,store email,otp,ttl-UserveifyDb

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    user_table = dynamodb.Table('User')
    verify_table = dynamodb.Table('UserVerify')
    useremail = event["email"]
    print(useremail)
    ##check email
    check = user_table.scan(
        ScanFilter={
            'email': {
                'AttributeValueList': [useremail],
                'ComparisonOperator': 'EQ'
            }
        })
    shouldinsert = check["Count"]
    success = False
    content = " "
    if shouldinsert > 0:
        content = "Your email has already existed!"
    ## generate otp. store into db(UserVerify),send email.
    else:
        ttl = int(time.time()) + 300
        otp = str(ttl)[-6:]
        dynamo_info = {
            "email": useremail,
            "Verification": otp,
            "ttl": ttl
        }
        json.dumps(dynamo_info)
        dynamo_data = {key: value for key, value in dynamo_info.items() if value}
        response = verify_table.put_item(Item=dynamo_data)
        ##send email
        SENDER = 'liszdeng@gmail.com'
        SENDERNAME = 'My Note'
        RECIPIENT = useremail
        USERNAME_SMTP = " #"
        PASSWORD_SMTP = " #"

        HOST = "email-smtp.us-east-1.amazonaws.com"
        PORT = 587
        SUBJECT = 'Welcome to Knock Note! Your verification code!'

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Welcome to Knock Note! Your verification code is\r\n"
                     )

        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Welcome to Knock Note! Your verification code is</h1>
          <p> """ + str(otp) + """<br><br>
            This email was sent with Amazon SES using the
            <a href='https://www.python.org/'>Python</a>
            <a href='https://docs.python.org/3/library/smtplib.html'>
            smtplib</a> library.</p>
        </body>
        </html>
                    """

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Try to send the message.
        try:
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
            server.close()
            print ("Email sent!")
            success = True
            content = "Verification code sent!"
        # Display an error message if something goes wrong.
        except Exception as e:
            print ("Error: ", e)

    return {
        'statusCode': 200,
        'body': {
            "success": success,
            "content": content

        }
    }


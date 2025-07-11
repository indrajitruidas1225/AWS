import json
import boto3
import os

ses = boto3.client('ses')

TO_EMAIL = os.environ['TO_EMAIL']

def lambda_handler(event, context):
    data = json.loads(event['body'])

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    email_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    response = ses.send_email(
        Source=TO_EMAIL,
        Destination={'ToAddresses': [TO_EMAIL]},
        Message={
            'Subject': {'Data': 'New Contact Form Submission'},
            'Body': {'Text': {'Data': email_body}}
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully!')
    }
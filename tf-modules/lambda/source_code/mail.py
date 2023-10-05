import smtplib
import boto3
from email.mime.text import MIMEText
from datetime import datetime,timedelta


def SendMail(subject,body):
    ses=boto3.client('ses')
    response = ses.send_email(
        Source='',
        Destination={
            'ToAddresses': [
            ]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Data': body
                }
            }
        }
    )
    print("Email Sent Successfully")
import json
from datetime import datetime
import pytz
import boto3
import re

def lambda_handler(event, context):
    try: 
        # Extract response status from the event
        db_data = event["Records"][0]["dynamodb"]
        response_status = db_data["NewImage"]["responseStatus"]["S"]
    except Exception as e:
        return None

    #Only rest of lambda function with response status == False
    if response_status != "False":
        return None

    # Extract data from the event
    task_id = db_data["Keys"]["ID"]["S"]
    cusomer_email = db_data["NewImage"]["customer"]["S"]
    date = db_data["NewImage"]["date"]["S"]
    generatedReply = db_data["NewImage"]["generatedReply"]["S"]
    local_datetime = change_Melbourne_time(date)

    #Identify DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('xxxxxx')

    #Extracting email components
    subject, body = process_email(generatedReply)
    print(type(subject), type(body))
 

    email = cusomer_email
    #Sending SES email
    try:
        ses_send_email(email, subject, body)
        print("email sent successful!")
    except Exception as e:
        print("email sent failed!")
        print(e)
        return None

    response = table.update_item(
    Key={
        'ID': task_id  # Partition key（ID）
    },
    UpdateExpression="SET responseStatus = :responseStatus, localDatetime = :local_datetime, generatedReply = :generatedReply, subject = :subject",
    ExpressionAttributeValues={
        ':responseStatus': 'True',
        ':local_datetime': local_datetime,
        ':generatedReply': body,
        ':subject': subject
    },
    ReturnValues="UPDATED_NEW"  
)
    print("Response status change successful!")

def change_Melbourne_time(time_string):
    try:
        original_time = datetime.strptime(time_string, "%a, %d %b %Y %H:%M:%S %z")

        # Set Melbourne timezone
        melbourne_tz = pytz.timezone('Australia/Melbourne')

        # Change time to Melbourne time
        melbourne_time = original_time.astimezone(melbourne_tz)

        # Formatting in ISO 8601
        iso_time = melbourne_time.isoformat()
        print("time change successful!")
        return iso_time
    except Exception as e:
        return time_string


def ses_send_email(email, subject, body):
    ses_client = boto3.client("ses", region_name="ap-southeast-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": email,
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": body,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": subject,
            },
        },
        Source="xxxxxx@xxxxxx",
    )
#Only work for my bedrock flow
def process_email(email):    

    #Regex to extract subject and body of generated email
    category1 = r'(?s)<category>(.*?)</category>'
    category2 = r'(?s)<category>\n(.*?)</category>'
    body1 = r'(?s)<answer>\n(.*?)</answer>'
    body2 = r'(?s)<answer>(.*?)</answer>'

    #Extracting email components
    if re.search(category1, email) == None:
        category_match = re.search(category2, email)[1]
    else:
        category_match = re.search(category1, email)[1]
    answer_match = re.search(body1, email)
    if re.search(body1, email) == None:
        answer_match = re.search(body2, email)[1]
    else:
        answer_match = re.search(body1, email)[1]
    category_match = str("Reply from CLUBLIME SOUTH YARRA regarding " + category_match)
    answer_match = str(answer_match.replace('[Your Name]',""))
    print(category_match)
    print(answer_match)
    return category_match, answer_match

import json
import base64
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
import boto3

def lambda_handler(event, context):
    print(event)
    
    #Identify DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('xxxxxx')

    #MessageID from sns as Partition key for DynamoDB
    task_id = event['Records'][0]['Sns']['MessageId']
    if check_message_exists(table, task_id):
        return None
    table.put_item(
        Item={
            'ID': task_id
        }
    )

    #Parse email from SNS
    raw_email = base64.b64decode(json.loads(event['Records'][0]['Sns']['Message'])["content"])
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)

    #Parse email subject
    subject = msg["subject"]
    print("subject")
    sender = msg["from"]
    print("sender")

    #Parse email body
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_content()
                print(body)
                break
            elif content_type == "text/html":
                body = part.get_content()
                print(body)
    else:
        body = msg.get_content()
        print(body)

    #Parse email datetime
    date_header = msg["date"]
    print(date_header)

    #Parse email sender
    from_header = msg["From"]
    if from_header:
        email_address = parseaddr(from_header)[1]
        print(email_address)
    else:
        print("No From Header Found")
    




    #Invoke Bedrock service to generate AI response
    prompt = f"{sender}; subject: {subject}; body: {body}"
    print(f"prompt is : {prompt}")
    reply_message = None
    while True:
        try:
            reply_message = invoke_bedrock(prompt)
            break
        #Handling bedrock error such as: "Too many requests, please wait before trying again."
        except Exception as e:
            reply_message = f'Failed to Generate response. Reason: {e} Retry...'

    #Save AI response to DynamoDB
    table.put_item(
        Item={
            'ID': task_id,
            'customer': email_address,
            'date': date_header,
            'customerEmail': prompt,
            'generatedReply': reply_message,
            #Sending generated email will be handle by another Lambda function and will change this accordingly
            'responseStatus': "False"
        }
    )


def check_message_exists(table, message_id):
    response = table.get_item(
        Key={
            'ID': message_id
        }
    )
    return 'Item' in response

def invoke_bedrock(prompt):

    #Identify bedrock agent
    bedrock_agent_runtime = boto3.client(service_name = 'bedrock-agent-runtime', region_name = 'ap-southeast-2')
    response = bedrock_agent_runtime.invoke_flow(

    #Identify flow
    flowIdentifier = "xxxxxxxxxxx",

    #Identify Alias in flow
    flowAliasIdentifier = "xxxxxxxxxxx",
    inputs = [
        { 
            "content": { 
                #Prompt send to bedrock
                "document": prompt
            },
            "nodeName": "FlowInputNode",
            "nodeOutputName": "document"
        }
    ]
)
    event_stream = response["responseStream"]
    respond = []
    for event in event_stream:
        respond.append(json.dumps(event, indent=2, ensure_ascii=False))
    
    #Parse genrated response
    reply_message = json.loads(respond[0]).get('flowOutputEvent').get('content').get('document')
    print(reply_message)
    return reply_message


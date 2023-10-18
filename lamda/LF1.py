import json
from datetime import datetime
import boto3
def lambda_handler(event, context):
    resp = {"statusCode": 200, "sessionState": event["sessionState"]}
    status = event["sessionState"]["intent"]["state"]
    if status == "Fulfilled":
        message = 'An email with my suggestions will be sent  to you shortly'
        resp['sessionState']['dialogAction']['message'] = {
            'contentType': 'PlainText',
            'content': message
        }
        #print(event["sessionState"]["intent"]['slots'])
        final = {}
        for i in  event["sessionState"]["intent"]['slots']:
            final[i] = event["sessionState"]["intent"]['slots'][i]['value']['interpretedValue']
            #final.append(event["sessionState"]["intent"]['slots'][i]['value']['interpretedValue'])
        formated  = json.dumps(final)
        print(formated)
        sqs_push(formated)
    ### worst case hard code them into a loop of the inital prompt for error check
    if "proposedNextState" not in event:
        resp["sessionState"]["dialogAction"] = {"type": "Close"}
    else:
        resp["sessionState"]["dialogAction"] = event["proposedNextState"][
        "dialogAction"
        ]
    return resp
def validate_time(time):
    # Is it in the future
    input_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    current_time = datetime.now()
    if input_time > current_time:
            return True  # The input time is in the future
    else:
            return False  # The input time is in the past
def validate_location(location):
    # is it in Manhattan NY
    if location !=None:
        location_str = location_str.lower()
        # Check if the location contains "manhattan, ny"
        return "manhattan, ny" in location_str
    else:
        return False
def validate_number_of_people(number):
    ### is it greater than 0?
    if number != None:
        return number >0
    else:
        return False    
def sqs_push(message):
    sqs = boto3.client('sqs',region_name='us-east-1')
    queue_name = "suggestions-queue"
    response = sqs.get_queue_url(QueueName='suggestions-queue')
    queue_url = response['QueueUrl']
    #https://stackoverflow.com/questions/74926354/botot3-with-sqs-the-address-queueurl-is-not-valid-for-this-endpoint
    # idk why this worked instead of below but I will take it
    #queue_url = 'sqs.us-east-1.amazonaws.com/239946977323/suggestions-queue'
    ##########################
    response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=message
    )
    ### sending message
    if 'MessageId' in response:
        message_id = response['MessageId']
        print(f"Message {message_id} sent successfully.")
    else:
        print("Failed to send the message. Check the response for errors.")




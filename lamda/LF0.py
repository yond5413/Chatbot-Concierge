import json
import boto3
# Define the client to interact with Lex
client = boto3.client('lexv2-runtime')
def lambda_handler(event, context):
    print("hell0")
    print(F"event {event}")
    print("#########")
    #msg_from_user = event['messages'][0]
    msg_from_user = event['messages']#[0]#['unstructured']['text']
    print(f'layer1: {msg_from_user}')
    msg_from_user = msg_from_user[0]['unstructured']
    print(f'layer2: {msg_from_user}')
    msg_from_user = msg_from_user['text']
    print(f'layer3: {msg_from_user}')
    # change this to the message that user submits on
    # your website using the 'event' variable
    #msg_from_user = "Hello"
    print(f"Message from frontend: {msg_from_user}")
    # Initiate conversation with Lex
    response = client.recognize_text(
        botId='5EG3DQPDWR',       #'ABCDEFGHIJK', # MODIFY HERE
        botAliasId='FPDSCTIAC0', #'ABCDEFGHIJK', # MODIFY HERE
        localeId='en_US',
        sessionId='testuser',
        text=msg_from_user)
    msg_from_lex = response.get('messages', [])
    if msg_from_lex:
        print(f"Message from Chatbot: {msg_from_lex[0]['content']}")
       
        resp = {
        'statusCode': 200,
        "messages": [
    {
      "type": "unstructured",
      "unstructured": {
        #"id": "string",
        "text": msg_from_lex[0]['content'],#"Work in progress comeback soon",
        #"timestamp": "string"
      }
    }
    ]
        #'body': "Hello from LF0!"
        }
        # modify resp to send back the next question Lex would ask from the user
        # format resp in a way that is understood by the frontend
        # HINT: refer to function insertMessage() in chat.js that you uploaded
        # to the S3 bucket
        return resp
    
    ##### working before lex added
    '''# TODO implement
    print(event)
    print(context)
    
       return {
        'statusCode': 200,
        "messages": [
    {
      "type": "unstructured",
      "unstructured": {
        "id": "string",
        "text": "Work in progress comeback soon",
        "timestamp": "string"
      }
    }
    ]
    }'''
    
    ## changes to LF0 doesn't need new sdk
    ## only changes required if you change api gateway
    ''''{
        'statusCode': 200,
        'body': json.dumps('Still working on it!')
    }'''

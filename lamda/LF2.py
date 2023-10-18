import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
REGION = 'us-east-1'
HOST = 'search-restaurants-6onrn3ewsxx34puurqayhmag64.us-east-1.es.amazonaws.com'
INDEX = 'restaurants'
def lambda_handler(event, context):
    ###TODO
    # after queue implemented
    # pop and access info about them using cusine  
    ## then access db for more info
    ### after that send email with sugesstions and info ig
    #print('Received event: ' + json.dumps(event))
    sqs_res = sqs_accesss()
    #print(sqs_res)
    #if sqs_res == None:
    #    sqs_res = {"Cuisine": "Italian", "Dining_Time": "2023-10-17", "Location": "Manhattan", "Number_of_people": "2", "email": "yond12399@gmail.com"}
    if sqs_res:
        #sqs_res-> has info from lex 
        # sample sqs
        results = query(sqs_res['Cuisine'])
        res =results[:3]
        ids = []
        queries = []
        for search in res:
            ids.append(search["Item"]['BusinessID']['S'])
            #print(search["Item"]['BusinessID']['S'])
            queries.append(lookup_data({'business_id': search["Item"]['BusinessID']['S']}))
        resp = email_formating(info = sqs_res,sugges = queries)
        #email_formating()
        return {
        'statusCode': 200,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps({'results': resp})
        }
    else:
        ### basic for testing 
        results = query('Mexican')
        #data = json.loads(results)
        print(results)
        #print(f"res: {results[0]},is also {type(results[0])}")
        #print(results[0]["Item"])
        #type = results[0]["Item"]#['S']
        #print(f"type: {type.keys()}")
        #business_id = results[0]["Item"]['BusinessID']['S']
        res =results[:3]
        ids = []
        queries = []
        for search in res:
            ids.append(search["Item"]['BusinessID']['S'])
            #print(search["Item"]['BusinessID']['S'])
            queries.append(lookup_data({'business_id': search["Item"]['BusinessID']['S']}))
        resp = email_formating(sugges = queries)
        return {
        'statusCode': 200,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps({'results': resp})
        }
def query(term):
    q = {'size': 5, 'query': {'multi_match': {'query': term}}}
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)
    res = client.search(index=INDEX, body=q)
    print(res)
    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])
    ###use hits to lookup in dynamo db
    ### format for email and send
    return results
def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
        cred.secret_key,
        region,
        service,
        session_token=cred.token)
############Dynamo-DB access########################
# should just be lookup tbh for more info
import boto3
from botocore.exceptions import ClientError
def lookup_data(key, db=None, table='yelp-restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
       # print(response['Item'])
        return response['Item']
####################################################
############### SES->email #########################
### once we get suggestion it is just formating a string after
### the email is verified
####################################################
import boto3
from botocore.exceptions import NoCredentialsError
def sqs_accesss():
    sqs = boto3.client('sqs',region_name='us-east-1')
    queue_name = "suggestions-queue"
    response = sqs.get_queue_url(QueueName='suggestions-queue')
    queue_url = response['QueueUrl']
    #https://stackoverflow.com/questions/74926354/botot3-with-sqs-the-address-queueurl-is-not-valid-for-this-endpoint
    # idk why this worked instead of below but I will take it
    #queue_url = 'sqs.us-east-1.amazonaws.com/239946977323/suggestions-queue'
    ##########################
    response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1  # Adjust as needed
    )
    #print(response)
    message = response.get('Messages', [])#[0]# if response.get('Messages') else None
    #print(message)
    ret = {}
    if message:
        data = message['Body']
        message_data = json.loads(body)
        # Process the message data as a dictionary
        cuisine = message_data['Cuisine']
        dining_time = message_data['Dining_Time']
        location = message_data['Location']
        number_of_people = message_data['Number_of_people']
        email = message_data['email']
        #ret = {}
        ret['Cuisine'] = cusine
        ret['Dining_Time'] = dining_time
        ret['Location'] = location
        ret['Number_of_people'] = number_of_people
        ret['email'] = email
        
        # Process the message content
        # Delete the message from the queue once processed
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    else:
        print("No message received")
    return ret 
def email_formating(info = None,sugges = None):
    ses = boto3.client('ses', region_name='us-east-1')
    sender_email = 'yd2696@columbia.edu'
    subject = 'Restaurant Suggestions'
    if info == None:
    ############ testing ####################    
        recipient_email = 'yond12399@gmail.com'## will be specified by lexbot from queue later
        email_body = f"Hello! Here are my restaurant suggestions for 2 people, for today at 7 pm:\n\n"
        for i in range(0,len(sugges)):
            data = sugges[i]
            email_body += f"{i+1}. {data['name']}, located at {data['address']}\n"
        email_body += "Enjoy your meal!"
        # Create the email message
        email_message = {
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': email_body}},
        }
        # Send the email
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [recipient_email]},
                Message=email_message
            )
            print("Email sent successfully!")
        except NoCredentialsError:
            print("AWS credentials not available or invalid.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
    ###### using info from elastic search 
        ret = ''
        #{"Cuisine": "Italian", "Dining_Time": "2023-10-17", "Location": "Manhattan", "Number_of_people": "2", "email": "yond12399@gmail.com"}
        recipient_email = info['email']## will be specified by lexbot from queue later
        email_body = f"Hello! Here are my {info['Cuisine']} restaurant suggestions for {info['Number_of_people']} people, for {info['Dining_Time']} :\n\n"
        for i in range(0,len(sugges)):
            data = sugges[i]
            email_body += f"{i+1}. {data['name']}, located at {data['address']}\n"
        email_body += "Enjoy your meal!"
        # Create the email message
        email_message = {
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': email_body}},
        }
        # Send the email
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [recipient_email]},
                Message=email_message
            )
            print("Email sent successfully!")
        except NoCredentialsError:
            print("AWS credentials not available or invalid.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [recipient_email]},
                Message=email_message
            )
            ret = "Email sent successfully!"
        except NoCredentialsError:
            ret ="AWS credentials not available or invalid."
        except Exception as e:
            ret= f"An error occurred: {str(e)}"
        return ret
    

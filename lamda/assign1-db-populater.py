import json
import boto3
import datetime
import csv
import os

def lambda_handler(event, context):
    # Specify the S3 bucket and file key
    bucket_name = 'my-chatbot-cc-bd'
    file_key = 'restaurant_data.csv'

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Download the CSV file from S3
    local_file_path = '/tmp/restaurant_data.csv'  # Use /tmp/ for Lambda's writable directory
    s3.download_file(bucket_name, file_key, local_file_path)

    # Read data from the downloaded CSV file
    data = []

    with open(local_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists
        for row in csv_reader:
            # Add an 'insertedAtTimestamp' column with the current timestamp
            row.append(str(datetime.datetime.now()))
            data.append(row)

    # Insert the data into DynamoDB
    insert_data(data)

    # Clean up the downloaded file (optional)
    os.remove(local_file_path)

    return "Data inserted into DynamoDB successfully."

def insert_data(data_list, db=None, table='yelp-restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    dynamodb_data = [{'business_id': row[0], 'name': row[1], 'address': row[2], 'review_count': row[3], 'rating': row[4], 'zipcode': row[5], 'cuisine': row[6], 'insertedAtTimestamp': row[7]} for row in data_list]
# overwrite if the same index is provided
    for data in dynamodb_data:#data_list:
        response = table.put_item(Item=data)
        print('@insert_data: response', response)
    return response

    

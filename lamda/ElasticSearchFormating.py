import json
import pandas as pd

# Load the restaurant data from the CSV file into a Pandas DataFrame
restaurant_data = pd.read_csv('restaurant_data.csv')

# Initialize an empty list to store the formatted data
formatted_data = []

# Counter for the sequential index
counter = 1

# Iterate through the restaurant data and format it
for index, row in restaurant_data.iterrows():
    # Create the 'index' part with "_id" and "_index" values
    index_part = {"index": {"_index": "restaurants", "_id": str(counter)}}
    
    # Create the document part with the restaurant data
    item_part = {
        "Item": {
            "Type": {"S": row['cuisine']},
            "BusinessID": {"S": row['business_id']}
        }
    }
    
    # Append both parts to the formatted data list
    formatted_data.append(index_part)
    formatted_data.append(item_part)
    
    # Increment the counter
    counter += 1

# Save the formatted data to a JSON file
with open('formatted_data.json', 'w') as json_file:
    for item in formatted_data:
        json.dump(item, json_file)
        json_file.write('\n')

import requests
import pandas as pd

api_key = '6p2hqkXqPdXdFVijKKzZ6slYu24bJidFf10Bs3K38_Ss7odl6CDCUWDwrHyW0wistbszljlr_4JZ6a-rNTp-6AsCIe8Y0xQfKaSOJDt3xh-WGYaTiVHCLB4ESTkoZXYx'
base_url = 'https://api.yelp.com/v3/businesses/search'
headers = {
    'Authorization': f'Bearer {api_key}',
}
location = 'Manhattan, NY'  # Replace with your desired location

#categories = 'Italian,Mexican,Chinese,Japanese,Indian,French,Mediterranean'
categories = '''
    Italian,
    Mexican,
    Chinese,
    Japanese,
    Indian,
    French,
    Mediterranean,
    Thai,
    Vietnamese,
    Korean,
    Spanish,
    Greek,
    Ethiopian,
    Peruvian,
    Cajun/Creole,
    Brazilian,
    African,
    Caribbean,
    Nepali/Tibetan,
    Irish,
    Turkish,
    Russian
'''

desired_count = 5000  # Collect 1000 restaurants for each category

# Initialize an empty list to store restaurant data
restaurant_data = []

for offset in range(0,1000,50):#desired_count, 50):
    params = {
        'categories': categories,
        'location': location,
        'limit': 50,
        'offset': offset,
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        businesses = data['businesses']

        for restaurant in businesses:
            # Extract the Yelp business ID
            business_id = restaurant['id']

            # Check if the restaurant is already in the list (not a duplicate)
            if business_id not in [r['business_id'] for r in restaurant_data]:
                # Add the restaurant data to the list
                restaurant_data.append({
                    'business_id': business_id,
                    'name': restaurant['name'],
                    'address': restaurant['location']['address1'],
                    'review_count': restaurant['review_count'],
                    'rating': restaurant['rating'],
                    'zipcode': restaurant['location']['zip_code'],
                    'cuisine': next((cat['title'] for cat in restaurant['categories'] if cat['title'] in categories), 'Other')
                })

    else:
        print(f"Request for offset {offset} failed with status code {response.status_code}")

# Create a Pandas DataFrame
restaurant_data_df = pd.DataFrame(restaurant_data)

# Set 'business_id' as the index
restaurant_data_df.set_index('business_id', inplace=True)

# Save the DataFrame to a CSV file
restaurant_data_df.to_csv('restaurant_data.csv')






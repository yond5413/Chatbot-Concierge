import pandas as pd

# Load your DataFrame from the CSV file or any other source
restaurant_data = pd.read_csv('restaurant_data.csv')

# Check for unique rows
original_shape = restaurant_data.shape
deduplicated_data = restaurant_data.drop_duplicates()
deduplicated_shape = deduplicated_data.shape

if original_shape == deduplicated_shape:
    print("The DataFrame has no duplicate rows.")
else:
    print("Duplicate rows were found and removed.")

duplicates = restaurant_data.duplicated(subset='business_id', keep='first')

# Get the duplicate rows
duplicate_data = restaurant_data[duplicates]

# Print the duplicate rows
print("Duplicate Rows:")
print(duplicate_data.shape)
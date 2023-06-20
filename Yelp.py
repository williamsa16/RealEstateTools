import requests

# Set up your Yelp API key
api_key = 'F91FwnEL-19Q0FezJOUf-1kGepVxiHiKznIFuEjTClUD4-Mk2H-7HGMf0E3h4M_fw6LKZhbTtfwmWyJaKY_TWT9ufhCQZK1R9mzOd8VuE2li93RL5UPOXa-XO3-QZHYx'

# Define the search parameters
location = '32202'  # ZIP code
term = 'restaurants'
radius = 24140  # 15 miles in meters
sort_by = 'rating'  # Sort by rating in descending order
limit = 50

# Set up the API request URL
url = f'https://api.yelp.com/v3/businesses/search?term={term}&location={location}&radius={radius}&sort_by={sort_by}&limit={limit}'

# Set the API key in the request headers
headers = {'Authorization': f'Bearer {api_key}'}

# Send the API request
response = requests.get(url, headers=headers)

# Parse the JSON response
data = response.json()

# Access the business information
businesses = data['businesses']

# Print the business names and ratings
for business in businesses:
    name = business['name']
    rating = business['rating']
    print(f'{name}: {rating}')
import requests
import pandas as pd

# Define the API endpoint and parameters
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    'vs_currency': 'usd',
    'days': '1',  # '1' for 24 hours, or use 'max' for all available data
    'interval': 'minutely'  # Correct interval value
}

# Fetch the data
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data)  # Print the data structure

    # Ensure the 'prices' key is in the response
    if 'prices' in data:
        # Extract prices
        prices = data['prices']
        
        # Convert to DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Display the DataFrame
        print(df.head())
        
        # Optionally save to CSV
        df.to_csv('bitcoin_minute_prices.csv', index=False)
    else:
        print("Key 'prices' not found in the API response")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")

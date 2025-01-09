import requests
import pandas as pd
from datetime import datetime
import os

# Convert a date string to milliseconds
def date_to_milliseconds(date_str):
    return int(pd.Timestamp(date_str).timestamp() * 1000)

# Fetch historical data from Binance
def fetch_historical_data(symbol, interval, start_date, file_path):
    start_time = date_to_milliseconds(start_date)
    end_time = int(datetime.now().timestamp() * 1000)
    print(f"Fetching data from {start_date} to {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (current time).")
    url = 'https://api.binance.com/api/v3/klines'
    all_data = []

    while start_time < end_time:
        # Fetch maximum allowed data in a single request
        response = requests.get(url, params={
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': min(start_time + (1000 * 8 * 60 * 60 * 1000), end_time),  # Fetch ~1000 intervals
            'limit': 1000
        }).json()
        if not response:
            break
        all_data.extend(response)
        start_time = response[-1][0] + 1  # Move start time forward

    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_'
    ])[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv(file_path, index=False)
    print(f"Data successfully saved to {file_path}")

# Configuration
symbol = 'BTCUSDT'
interval = '8h'
start_date = '2019-07-01'  # Change this as needed
file_path = r'C:\Users\91759\Downloads\cryptopredictions\binance.csv'

# Remove file if it exists
if os.path.exists(file_path):
    os.remove(file_path)

# Fetch and save data
fetch_historical_data(symbol, interval, start_date, file_path)
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load data
file = r'C:\Users\91759\Downloads\cryptopredictions\binance.csv'
df = pd.read_csv(file)

# Define features (X) and target (y)
X = df[['open', 'high', 'low', 'volume']]
y = df['close']

# Train linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the most recent row of features for prediction
new_data = df[['open', 'high', 'low', 'volume']].tail(1)
print(f"New data for prediction:\n{new_data}")

# Actual close price for the same row
n2 = df['close'].tail(1)
print(f"Actual closed price: {n2.values[0]}")

# Predict the close price using the features
predicted = model.predict(new_data)
print(f"Predicted close price: {predicted[0]}")
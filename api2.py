import requests
import pandas as pd
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Function to get historical klines from Binance
def get_historical_klines(symbol, interval, start_time, end_time=None):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Max limit per request
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Convert a date string to milliseconds
def date_to_milliseconds(date_str):
    return int(pd.Timestamp(date_str).timestamp() * 1000)

# Fetch 5 years of data
symbol = 'BTCUSDT'
interval = '8h'
start_date = '2019-07-23'  # Adjust this to 5 years back from today
current_time = datetime.now()
start_time = date_to_milliseconds(start_date)
end_time = (int(current_time.timestamp() * 1000))+720000

# Fetch data in chunks
data = []
while start_time <= end_time:
    new_data = get_historical_klines(symbol, interval, start_time, end_time)
    if not new_data:
        break
    data.extend(new_data)
    # Update start_time to the timestamp of the last fetched data plus one millisecond
    start_time = new_data[-1][0] + 1
    # Avoid hitting rate limits
    time.sleep(0.5)

# Convert data to DataFrame
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
           'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
           'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(data, columns=columns)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Select relevant columns
df = df[['open', 'high', 'low', 'close', 'volume']]
df = df.astype(float)

# Path to your CSV file
file_path = 'binance_btcusdt_5years.csv'

# Check if the file exists and delete if it does
if os.path.exists(file_path):
    os.remove(file_path)

# Save DataFrame to a CSV file
df.to_csv(file_path)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'])
plt.title('Bitcoin Price (Last 5 Years)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()

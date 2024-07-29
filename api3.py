import asyncio
import websockets
import json
import pandas as pd

async def fetch_data():
    uri = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1h'
    async with websockets.connect(uri) as websocket:
        latest_data = None
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            kline = data['k']
            timestamp = pd.to_datetime(kline['t'], unit='ms')
            open_price = float(kline['o'])
            high_price = float(kline['h'])
            low_price = float(kline['l'])
            close_price = float(kline['c'])
            volume = float(kline['v'])
            
            # Only update the latest_data if the timestamp is more recent
            if latest_data is None or timestamp > latest_data['timestamp']:
                latest_data = {
                    'timestamp': timestamp,
                    'open': open_price,
                    'high': high_price,
                    'low': low_price,
                    'close': close_price,
                    'volume': volume
                }
            
            # Print the latest data
            if latest_data:
                print(f"Timestamp: {latest_data['timestamp']}, Open: {latest_data['open']}, High: {latest_data['high']}, Low: {latest_data['low']}, Close: {latest_data['close']}, Volume: {latest_data['volume']}")

# Run the asyncio event loop
asyncio.get_event_loop().run_until_complete(fetch_data())

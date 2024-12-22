from django.shortcuts import render, redirect
from .forms import Selectalgorithm, SelectCoin, SelectDuration
from users.forms import FeedbackForm
import os
import pandas as pd
from datetime import datetime
import requests
from sklearn.linear_model import LinearRegression
from django.conf import settings

# Utility function to convert a date string to milliseconds
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

# View function
def predicts(request):
    form_feedback = FeedbackForm()
    forma = Selectalgorithm()
    formb = SelectCoin()
    formc = SelectDuration()
    predicted_close=''

    if request.method == 'POST':
        forma = Selectalgorithm(request.POST)
        formb = SelectCoin(request.POST)
        formc = SelectDuration(request.POST)
        form_feedback = FeedbackForm(request.POST)
        if forma.is_valid():
            print("Selected algorithm:", forma.cleaned_data['item'])
        if formb.is_valid():
            print("Selected coin:", formb.cleaned_data['item'])
        if formc.is_valid():
            print("Selected duration:", formc.cleaned_data['item'])
            


        if forma.is_valid() and formb.is_valid() and formc.is_valid():
            print('item')
            selected_item = forma.cleaned_data['item']  # Ensure field names match your form
            selected_coin = formb.cleaned_data['item']
            selected_duration = formc.cleaned_data['item']
            print("Algorithm:", selected_item.al_name)
            print("Coin:", selected_coin.c_name)
            print("Duration:", selected_duration.time)

            # Configuration
            symbol = str(selected_coin) + 'USDT'
            interval = str(selected_duration)
            print(symbol,interval)
            start_date = '2019-07-01'
            file_path = os.path.join(settings.MEDIA_ROOT, 'binance.csv')

            # Remove the file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            # Fetch and save data
            fetch_historical_data(symbol, interval, start_date, file_path)

            # Load data and train model
            df = pd.read_csv(file_path)
            X = df[['open', 'high', 'low', 'volume']]
            y = df['close']

            model = LinearRegression()
            model.fit(X, y)

            # Prepare prediction
            new_data = df[['open', 'high', 'low', 'volume']].tail(1)
            actual_close = df['close'].tail(1).values[0]
            predicted_close = model.predict(new_data)[0]

            print(f"New data for prediction:\n{new_data}")
            print(f"Actual closed price: {actual_close}")
            print(f"Predicted close price: {predicted_close}")
        else:
            predicted_close = None

        # Save feedback if valid
        if form_feedback.is_valid():
            feedback = form_feedback.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('predicts')
    
    return render(request, "predict.html", {
        'forma': forma,
        'formb': formb,
        'formc': formc,
        'form': form_feedback,
        'predict': predicted_close
    })

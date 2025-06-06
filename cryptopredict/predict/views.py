from django.shortcuts import render, redirect
from .forms import Selectalgorithm, SelectCoin, SelectDuration
from users.forms import FeedbackForm
import os
import pandas as pd
from datetime import datetime
import requests
from django.contrib.auth.decorators import login_required
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
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
@login_required(login_url='/account')
def predicts(request):
    form_feedback = FeedbackForm()
    forma = Selectalgorithm()
    formb = SelectCoin()
    formc = SelectDuration()
    predicted_clos=''
    predicted_close=''

    if request.method == 'POST':
        forma = Selectalgorithm(request.POST)
        formb = SelectCoin(request.POST)
        formc = SelectDuration(request.POST)
        form_feedback = FeedbackForm(request.POST)
        if forma.is_valid():
            print("Selected algorithm:", forma.cleaned_data['algorithm'])
        if formb.is_valid():
            print("Selected coin:", formb.cleaned_data['coin'])
        if formc.is_valid():
            print("Selected duration:", formc.cleaned_data['duration'])
            


        if forma.is_valid() and formb.is_valid() and formc.is_valid():
            selected_item = forma.cleaned_data['algorithm']  # Ensure field names match your form
            selected_coin = formb.cleaned_data['coin']
            selected_duration = formc.cleaned_data['duration']
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
            print(type(selected_item))
            if str(selected_item) == 'MLR': 
                model = LinearRegression()
                model.fit(X, y)

                # Prepare prediction
                new_data = df[['open', 'high', 'low', 'volume']].tail(1)
                actual_close = df['close'].tail(1).values[0]
                predicted_close = model.predict(new_data)[0]
                predicted_clos=str(predicted_close)[:8]

                print(f"New data for prediction:\n{new_data}")
                print(f"Actual closed price: {actual_close}")
                print(f"Predicted close price: {predicted_close}")
                print(type(predicted_close))
            elif str(selected_item) == 'BOOST':
                # Train Gradient Boosting Regressor model
                model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
                model.fit(X, y)

                # Get the most recent row of features for prediction
                new_data = df[['open', 'high', 'low', 'volume']].tail(1)
                print(f"New data for prediction:\n{new_data}")

                # Actual close price for the same row
                n2 = df['close'].tail(1)
                print(f"Actual closed price: {n2.values[0]}")
                print('GradientBoot')
                # Predict the close price using the features
                predicted = model.predict(new_data)
                print(f"Predicted close price: {predicted[0]}")
                predicted_close=predicted[0]
                predicted_clos=str(predicted_close)[:8]
            elif str(selected_item) == 'DECISION':
                # Train Random Forest Regressor model
                model = RandomForestRegressor(n_estimators=100, random_state=42)  # You can adjust n_estimators or other hyperparameters
                model.fit(X, y)

                # Get the most recent row of features for prediction
                new_data = df[['open', 'high', 'low', 'volume']].tail(1)
                print(f"New data for prediction:\n{new_data}")

                # Actual close price for the same row
                n2 = df['close'].tail(1)
                print(f"Actual closed price: {n2.values[0]}")
                print('decision')
                # Predict the close price using the features
                predicted = model.predict(new_data)
                print(f"Predicted close price: {predicted[0]}")
                predicted_close=predicted[0]
                predicted_clos=str(predicted_close)[:8]
            else:        
                predicted_clos = None

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
        'predict': predicted_clos
    })

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load data
file = r'C:\Users\yasmeen\Downloads\cryptopredictions-mains (1)\cryptopredictions-mains\binance.csv'
df = pd.read_csv("binance.csv")

# Define features (X) and target (y)
X = df[['open', 'high', 'low', 'volume']]
y = df['close']

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
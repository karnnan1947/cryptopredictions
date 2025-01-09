import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

# Load data
file = r'C:\Users\yasmeen\Downloads\cryptopredictions-mains (1)\cryptopredictions-mains\binance.csv'
df = pd.read_csv("binance.csv")

# Define features (X) and target (y)
X = df[['open', 'high', 'low', 'volume']]
y = df['close']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Support Vector Regression model
model = SVR(kernel='rbf')  # You can also try other kernels like 'linear' or 'poly'
model.fit(X_scaled, y)

# Get the most recent row of features for prediction
new_data = df[['open', 'high', 'low', 'volume']].tail(1)
print(f"New data for prediction:\n{new_data}")

# Scale the new data for prediction
new_data_scaled = scaler.transform(new_data)

# Actual close price for the same row
n2 = df['close'].tail(1)
print(f"Actual closed price: {n2.values[0]}")
print('svm')
# Predict the close price using the features
predicted = model.predict(new_data_scaled)
print(f"Predicted close price: {predicted[0]}")
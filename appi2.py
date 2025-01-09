import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

# Load data
file = r'C:\Users\91759\Downloads\cryptopredictions\binance.csv'
df = pd.read_csv(file)

# Define features (X) and target (y)
X = df[['open', 'high', 'low', 'volume']]  # Use the relevant columns (adjust if needed)
y = df['close']

# Feature scaling (MinMaxScaler)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Reshape for LSTM (requires 3D input)
X_scaled = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)

# Define LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))
model.add(Dense(units=1))  # Output layer

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the LSTM model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Prepare new data for prediction (make sure it has the same features used for training)
new_data = df[['open', 'high', 'low', 'volume']].tail(1)  # Adjust if you have more features

# Check if new_data has the same number of features (4 in this case)
if new_data.shape[1] != X.shape[1]:
    print(f"Feature mismatch: new data has {new_data.shape[1]} features, but the model was trained with {X.shape[1]} features.")
else:
    # Scale the new data using the same scaler
    scaled_new_data = scaler.transform(new_data)

    # Reshape for LSTM input (3D)
    scaled_new_data = scaled_new_data.reshape((scaled_new_data.shape[0], scaled_new_data.shape[1], 1))

    # Predict the close price using the trained model
    predicted_price = model.predict(scaled_new_data)
    print(f"Predicted close price: {predicted_price[0][0]}")

    # Actual close price for comparison (same row as the new data)
    actual_close_price = df['close'].tail(1).values[0]
    print(f"Actual close price: {actual_close_price}")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load the Data
data = pd.read_csv('bin.csv')

# Step 2: Preprocess the Data
data['timestamp'] = pd.to_datetime(data['timestamp'])
data = data.dropna()

# Define features and target
features = data[['open', 'high', 'low', 'close', 'volume']]  # Include 'close' as a feature for training
target = data['close']  # We'll predict the closing price

# Step 3: Split the Data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Step 4: Create the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Step 6: Make Predictions
# Use the most recent 'open', 'high', 'low', and 'volume' to predict the next 'close' price
new_data = data[['open', 'high', 'low', 'volume']].tail(1)  # Exclude 'close' for prediction

# Ensure new_data is in the correct format (DataFrame)
prediction = model.predict(new_data)
print(f'Predicted Closing Price for the next time period based on the last available data: {prediction[0]}')

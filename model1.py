import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load the Data
data = pd.read_csv('bin.csv')

# Step 2: Preprocess the Data
data['timestamp'] = pd.to_datetime(data['timestamp'])
data = data.dropna()
features = data[['open', 'high', 'low', 'close', 'volume']]
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
# Take the last row of the data as the new data
new_data = features.tail(1)

# Ensure new_data is a DataFrame
prediction = model.predict(new_data)
print(f'Predicted Closing Price for the last row of data: {prediction[0]}')

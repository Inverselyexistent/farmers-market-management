import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load your dataset (replace 'your_dataset.csv' with the actual file path)
data = pd.read_excel(r"D:\cropprediction.xlsx")

# Define the scaling factor for demand calculation (you can adjust this value)
scaling_factor = 0.1

# Create a proxy for demand: demand = quantity - (price * scaling_factor)
data['demand_proxy'] = data['quantity'] - (data['Price'] * scaling_factor)

# Use 'price' and 'quantity' as features for the demand model
X_demand = data[['Price', 'quantity']].values
y_demand = data['demand_proxy'].values  # Target: proxy demand

# Split the dataset into training and test sets for the demand model
X_train_demand, X_test_demand, y_train_demand, y_test_demand = train_test_split(X_demand, y_demand, test_size=0.2, random_state=42)

# Initialize and train the demand model
demand_model = LinearRegression()
demand_model.fit(X_train_demand, y_train_demand)

# Test the demand model
y_pred_demand = demand_model.predict(X_test_demand)
mse_demand = mean_squared_error(y_test_demand, y_pred_demand)
r2_demand = r2_score(y_test_demand, y_pred_demand)

print(f"Demand Model Mean Squared Error: {mse_demand:.2f}")
print(f"Demand Model R^2 Score: {r2_demand:.2f}")

# Use 'demand_proxy' (computed demand score) as the feature for the price recommendation model
X_price = data[['demand_proxy']].values
y_price = data['Price'].values  # Target: price

# Split data into training and testing sets for the price model
X_train_price, X_test_price, y_train_price, y_test_price = train_test_split(X_price, y_price, test_size=0.2, random_state=42)

# Train the price recommendation model (Random Forest Regressor)
price_model = RandomForestRegressor(n_estimators=100, random_state=42)
price_model.fit(X_train_price, y_train_price)

# Evaluate the price model
price_pred = price_model.predict(X_test_price)
price_rmse = np.sqrt(mean_squared_error(y_test_price, price_pred))
print(f"Price Model RMSE: {price_rmse:.2f}")
from tkinter import messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

# Load the dataset
file_path = r"D:\direct farm\farmers_market_data.csv"
df = pd.read_csv(file_path)

# Verify the structure of the dataset
print(df.head(), df.columns)

# Initialize label encoder and encode 'Commodity' column
label_encoder = LabelEncoder()
df['Commodity_encoded'] = label_encoder.fit_transform(df['Commodity'])

# Calculate the Average Price for Demand Prediction
df['Avg Price (Rs/Quintal)'] = (df['Min Price (Rs/Quintal)'] + df['Max Price (Rs/Quintal)']) / 2

# Model 1: Price Prediction Model (Regression)
X_price = df[['Commodity_encoded', 'Modal Price (Rs/Quintal)']]
y_price = df['Avg Price (Rs/Quintal)']
X_price_train, X_price_test, y_price_train, y_price_test = train_test_split(X_price, y_price, test_size=0.2, random_state=42)

# Train regression model for price prediction
price_model = LinearRegression()
price_model.fit(X_price_train, y_price_train)
y_price_pred = price_model.predict(X_price_test)
mse_price = mean_squared_error(y_price_test, y_price_pred)
print(f"Price Prediction Model MSE: {mse_price}")

# Model 2: Demand Prediction Model (Classification)
df['Price_Difference'] = abs(df['Avg Price (Rs/Quintal)'] - df['Modal Price (Rs/Quintal)'])
df['Demand'] = df['Price_Difference'].apply(lambda x: 'High' if x <= 1000 else 'Low')

# Prepare features and target for demand prediction model
X_demand = df[['Avg Price (Rs/Quintal)', 'Modal Price (Rs/Quintal)']]
y_demand = df['Demand']
X_demand_train, X_demand_test, y_demand_train, y_demand_test = train_test_split(X_demand, y_demand, test_size=0.2, random_state=42)

# Train demand prediction classifier
demand_model = DecisionTreeClassifier()
demand_model.fit(X_demand_train, y_demand_train)
y_demand_pred = demand_model.predict(X_demand_test)
accuracy_demand = accuracy_score(y_demand_test, y_demand_pred)
print(f"Demand Prediction Model Accuracy: {accuracy_demand}")

# Predict recommended price function
def predict_recommended_price(commodity, modal_price):
    try:
        commodity_encoded = label_encoder.transform([commodity])[0]
        recommended_price = price_model.predict([[commodity_encoded, modal_price]])[0]
        return recommended_price
    except ValueError as e:
        messagebox.showerror("Error", f"Commodity '{commodity}' not found in encoding.")
        return None

# Predict demand function
def predict_demand(user_price, recommended_price):
    demand = demand_model.predict([[user_price, recommended_price]])[0]
    return demand

# Example usage
user_commodity = 'Banana'  # Example user input for commodity
user_modal_price = 2500  # Example modal price input by the user

# Predict recommended price
def predict_recommended_price(commodity, modal_price):
    commodity_encoded = label_encoder.transform([commodity])[0]
    recommended_price = price_model.predict([[commodity_encoded, modal_price]])[0]
    return recommended_price
# Display the first few rows of the original and encoded columns
print(df[['Commodity', 'Commodity_encoded']].head())
# Display unique values in the 'Commodity_encoded' column
print(df['Commodity_encoded'].unique())

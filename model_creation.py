# model_creation.py

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# Initialize models
demand_model = LinearRegression()
price_model = DecisionTreeRegressor()

# Train the demand model
def train_demand_model():
    prices = np.array([10, 15, 20, 25, 30, 35])
    quantities = np.array([100, 90, 85, 75, 60, 55])
    demand_scores = np.array([80, 75, 70, 65, 55, 50])
    X_demand = np.column_stack((prices, quantities))
    y_demand = demand_scores
    demand_model.fit(X_demand, y_demand)

# Train the price model
def train_price_model():
    demand_scores = np.array([80, 75, 70, 65, 55, 50])
    optimal_prices = np.array([12, 16, 19, 23, 28, 34])
    X_price = demand_scores.reshape(-1, 1)
    y_price = optimal_prices
    price_model.fit(X_price, y_price)

# Call training functions to train models
train_demand_model()
train_price_model()

# Functions to access trained models
def predict_demand_score(price, quantity):
    demand_features = np.array([[price, quantity]])
    return demand_model.predict(demand_features)[0]

def recommend_price(demand_score):
    return price_model.predict(np.array([[demand_score]]))[0]

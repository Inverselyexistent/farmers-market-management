# Import required libraries
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset
file_path = r"D:\direct farm\farmers_market_data.csv"
df = pd.read_csv(file_path)

# Step 1: Initial Inspection of Data
print("Initial Data Overview:\n", df.head())
print("\nSummary of Dataset Information:")
df.info()

# Step 2: Handle Missing Values
# Check for missing values in each column
print("\nMissing Values in Each Column:\n", df.isnull().sum())
# Here, if there were any missing values, we would handle them accordingly (e.g., filling with mean/median or removing rows).
# Assuming no missing values as observed initially.

# Step 3: Encoding Categorical Variables
# Initialize LabelEncoder for categorical columns
label_encoder = LabelEncoder()
categorical_columns = ['District Name', 'Market Name', 'Commodity', 'Variety', 'Grade']

# Encode each categorical column and add as new columns with "_encoded" suffix
for column in categorical_columns:
    df[column + '_encoded'] = label_encoder.fit_transform(df[column])

# Step 4: Feature Engineering - Calculating Average Price
# Create an "Avg Price" column as the mean of "Min Price" and "Max Price"
df['Avg Price (Rs/Quintal)'] = (df['Min Price (Rs/Quintal)'] + df['Max Price (Rs/Quintal)']) / 2

# Step 5: Checking for Outliers
# Visualize "Min Price", "Max Price", and "Modal Price" to identify potential outliers
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[['Min Price (Rs/Quintal)', 'Max Price (Rs/Quintal)', 'Modal Price (Rs/Quintal)']])
plt.title("Boxplot of Prices to Detect Outliers")
plt.show()

# Step 6: Scaling Numeric Features
# Standardize numerical features for machine learning if needed
scaler = StandardScaler()
numeric_features = ['Min Price (Rs/Quintal)', 'Max Price (Rs/Quintal)', 'Modal Price (Rs/Quintal)', 'Avg Price (Rs/Quintal)']
df_scaled = df.copy()
df_scaled[numeric_features] = scaler.fit_transform(df[numeric_features])


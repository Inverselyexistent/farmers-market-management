import pandas as pd

# Load the Excel file
file_path = r"D:\cropprediction.xlsx"
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe
print(data.head())
# Check for missing values
print(data.isnull().sum())

# Check data types
print(data.dtypes)

# Get basic statistics
print(data.describe())

# Example: Fill missing values with the mean of the column
data.fillna(data.mean(), inplace=True)

# Or drop rows with missing values
# data.dropna(inplace=True)
# Example: Convert categorical variables using one-hot encoding
data = pd.get_dummies(data, drop_first=True)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Convert back to DataFrame
data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
data_scaled.to_excel(r"D:\cropprediction_preprocessed.xlsx", index=False)
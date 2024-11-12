import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the Excel file
file_path = r"D:\cropprediction.xlsx"
data = pd.read_excel(file_path)
print("Data loaded successfully.")

# Identify categorical and numerical columns
categorical_columns = data.select_dtypes(include=['object']).columns
numeric_columns = data.select_dtypes(include=['number']).columns
print("\nCategorical columns identified:", list(categorical_columns))
print("\nNumerical columns identified:", list(numeric_columns))

# Fill missing values in numerical columns with the mean
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
print("\nMissing values in numerical columns filled with the mean.")

# Fill missing values in categorical columns with a placeholder
data[categorical_columns] = data[categorical_columns].fillna("Unknown")
print("\nMissing values in categorical columns filled with 'Unknown'.")

# Convert categorical columns to one-hot encoding and cast to integers
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True).astype(int)
print("\nCategorical columns converted to one-hot encoding.")

# Standardize numeric columns only
scaler = StandardScaler()
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
print("\nNumerical columns standardized.")

# Display a preview of the final preprocessed data
print("\nPreview of the preprocessed data:")
print(data.head())

# Save the preprocessed data to a new Excel file
data.to_excel(r"D:\cropprediction_preprocessed.xlsx", index=False)
print("\nPreprocessed data has been saved to 'cropprediction_preprocessed.xlsx'")





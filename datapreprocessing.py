import pandas as pd

# Load the dataset from the downloaded CSV file
data_file = r"C:\Users\suhan\Downloads\cleaned_crop_production.csv"
df = pd.read_csv(data_file)

# Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# Handle missing values (example: filling missing values in 'Production' column with 0)
if 'Production' in df.columns:
    df['Production'].fillna(0, inplace=True)

# Data type conversion if needed (example: converting 'Year' to integer)
if 'Year' in df.columns:
    df['Year'] = df['Year'].astype(int)

# Drop irrelevant columns if any (e.g., 'Area of Cultivation' if not needed)
df.drop(columns=['Area of Cultivation'], errors='ignore', inplace=True)

# Save pre-processed data
cleaned_file = "cleaned_crop_production_stats.csv"
df.to_csv(cleaned_file, index=False)
print("Data preprocessing completed successfully.")

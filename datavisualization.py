import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
cleaned_file = r"C:\Users\suhan\Downloads\cleaned_crop_production.csv"  # Update the path if necessary
df = pd.read_csv(cleaned_file)

# Basic data overview
print("Data Overview:")
print(df.describe(include='all'))

# Visualization 1: Production Over Time
if 'Arrival_Date' in df.columns and 'Modal_x0020_Price' in df.columns:
    df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], errors='coerce')  # Convert to datetime
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='Arrival_Date', y='Modal_x0020_Price', errorbar=None)
    plt.title('Modal Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Modal Price')
    plt.grid(True)
    plt.show()

# Visualization 2: Production by State (Top 10 states)
if 'State' in df.columns and 'Modal_x0020_Price' in df.columns:
    top_states = df.groupby('State')['Modal_x0020_Price'].mean().nlargest(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_states.index, y=top_states.values)
    plt.title('Top 10 States by Average Modal Price')
    plt.xlabel('State')
    plt.ylabel('Average Modal Price')
    plt.xticks(rotation=45)
    plt.show()

# Visualization 3: Production Distribution
if 'Modal_x0020_Price' in df.columns:
    plt.figure(figsize=(10, 5))
    sns.histplot(df['Modal_x0020_Price'], bins=30, kde=True, color='skyblue')
    plt.title('Modal Price Distribution')
    plt.xlabel('Modal Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Visualization 4: Correlation Heatmap
numeric_df = df.select_dtypes(include='number')  # Select only numeric columns
if numeric_df.shape[1] > 1:  # Ensure there is more than one numeric column
    plt.figure(figsize=(12, 8))
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()
else:
    print("Not enough numeric columns to create a correlation heatmap.")

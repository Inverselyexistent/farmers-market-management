# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
# Load the dataset
file_path = r"D:\direct farm\farmers_market_data.csv"
df = pd.read_csv(file_path)

sns.set(style="whitegrid")

# 1. Distribution of Modal Price
plt.figure(figsize=(10, 6))
sns.histplot(df['Modal Price (Rs/Quintal)'], bins=20, kde=True, color='orange')
plt.title("Distribution of Modal Price (Rs/Quintal)")
plt.xlabel("Modal Price (Rs/Quintal)")
plt.ylabel("Frequency")
plt.show()

# 2. Boxplot for Max Price per Commodity
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='Commodity', y='Max Price (Rs/Quintal)', palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Max Price per Commodity")
plt.xlabel("Commodity")
plt.ylabel("Max Price (Rs/Quintal)")
plt.show()

# 3. Modal Price Comparison across Commodities
plt.figure(figsize=(12, 8))
sns.barplot(data=df, x='Commodity', y='Modal Price (Rs/Quintal)', estimator=sum, ci=None, palette="plasma")
plt.xticks(rotation=45)
plt.title("Total Modal Price per Commodity")
plt.xlabel("Commodity")
plt.ylabel("Modal Price (Rs/Quintal)")
plt.show()

# 4. Count of Entries per District
plt.figure(figsize=(14, 7))
sns.countplot(data=df, y='District Name', order=df['District Name'].value_counts().index, palette="Blues_r")
plt.title("Number of Entries per District")
plt.xlabel("Count")
plt.ylabel("District Name")
plt.show()

# Select specific columns for visualization
columns_to_use = ['Modal Price (Rs/Quintal)', 'Min Price (Rs/Quintal)', 'Max Price (Rs/Quintal)']

# Scaling the selected columns for pairplot visualization
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[columns_to_use] = scaler.fit_transform(df[columns_to_use])

# 5. Pairplot for Selected Price Columns
sns.pairplot(df_scaled[columns_to_use])
plt.suptitle("Pairplot for Selected Price Columns (Scaled)", y=1.02)
plt.show()

# 6. Correlation Heatmap for Selected Price Columns
plt.figure(figsize=(8, 6))
correlation = df_scaled[columns_to_use].corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap of Selected Price Columns")
plt.show()
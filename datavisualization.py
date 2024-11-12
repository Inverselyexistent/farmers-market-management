import pandas as pd

# Load the Excel file
file_path = r"D:\cropprediction.xlsx"
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe
print(data.head())
import matplotlib.pyplot as plt
import seaborn as sns

# Histogram of Price
plt.figure(figsize=(10, 6))
sns.histplot(data['Price'], bins=30, kde=True)
plt.title('Distribution of Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()
# Histogram of Quantity
plt.figure(figsize=(10, 6))
sns.histplot(data['quantity'], bins=30, kde=True)
plt.title('Distribution of Quantity')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.show()
# Box plot for Price
plt.figure(figsize=(10, 6))
sns.boxplot(y=data['Price'])
plt.title('Box Plot of Price')
plt.ylabel('Price')
plt.show()
# Box plot for Quantity
plt.figure(figsize=(10, 6))
sns.boxplot(y=data['quantity'])
plt.title('Box Plot of Quantity')
plt.ylabel('Quantity')
plt.show()
# Calculate the correlation matrix
correlation_matrix = data[['Price', 'quantity']].corr()
# Scatter plot between Price and Quantity
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Price', y='quantity', data=data)
plt.title('Scatter Plot of Price vs Quantity')
plt.xlabel('Price')
plt.ylabel('Quantity')
plt.show()
# Create a heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Heatmap')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'steam_user_games_data_filtered.csv'
data = pd.read_csv(file_path)

# Removing outliers based on the interquartile range (IQR) for total_hours_played
Q1 = data['total_hours_played'].quantile(0.25)
Q3 = data['total_hours_played'].quantile(0.75)
IQR = Q3 - Q1

# Define acceptable range without outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the data to exclude outliers
filtered_data = data[(data['total_hours_played'] >= lower_bound) & (data['total_hours_played'] <= upper_bound)]

# Group by category and calculate the total hours played for each category
category_hours = filtered_data.groupby('category')['total_hours_played'].sum()

# Plotting the histogram
plt.figure(figsize=(8, 6))
plt.bar(category_hours.index, category_hours, width=0.5)
plt.title('Total Hours Played per Category', fontsize=14)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Hours Played', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

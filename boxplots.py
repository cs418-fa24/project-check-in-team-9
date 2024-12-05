import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV files
df_casuals = pd.read_csv('Notebook/steam_user_games_data_casual.csv')
df_normies = pd.read_csv('Notebook/steam_user_games_data_normies.csv')
df_gamers = pd.read_csv('Notebook/steam_user_games_data_gamer.csv')


# Exclude accounts with 0 playtime
df_casuals = df_casuals[df_casuals['total_hours_account (hrs)'] > 0]
df_normies = df_normies[df_normies['total_hours_account (hrs)'] > 0]
df_gamers = df_gamers[df_gamers['total_hours_account (hrs)'] > 0]

# OPTIONAL: Log-transform the 'total_hours_account' column
# df_casuals['total_hours_account (hrs)'] = df_casuals['total_hours_account (hrs)'].apply(lambda x: np.log(x + 1) if x > 0 else 0)
# df_normies['total_hours_account (hrs)'] = df_normies['total_hours_account (hrs)'].apply(lambda x: np.log(x + 1) if x > 0 else 0)
# df_gamers['total_hours_account (hrs)'] = df_gamers['total_hours_account (hrs)'].apply(lambda x: np.log(x + 1) if x > 0 else 0)

# Create the figure
plt.figure(figsize=(12, 6))

# Create the box plots
box_casuals = plt.boxplot(df_casuals['total_hours_account (hrs)'].dropna(), vert=True, patch_artist=True, positions=[1])
box_normies = plt.boxplot(df_normies['total_hours_account (hrs)'].dropna(), vert=True, patch_artist=True, positions=[2])
box_gamers = plt.boxplot(df_gamers['total_hours_account (hrs)'].dropna(), vert=True, patch_artist=True, positions=[3])

# Set log scale on the y-axis to address wide range of data
plt.yscale('log')

# Label the boxes
plt.xticks([1, 2, 3], ['Casuals','Normies', 'Gamers'])

# Add a label for the median of each group
median_casuals = np.median(df_casuals['total_hours_account (hrs)'].dropna())
median_gamers = np.median(df_gamers['total_hours_account (hrs)'].dropna())
median_normies = np.median(df_normies['total_hours_account (hrs)'].dropna())


plt.text(1, median_casuals, f'Median: {median_casuals:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=12, color='red')
plt.text(2, median_normies, f'Median: {median_normies:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=12, color='red')
plt.text(3, median_gamers, f'Median: {median_gamers:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=12, color='red')


# Add labels and title
plt.title('Box Plot of Total Hours for Casuals, Normies, and Gamers')
plt.ylabel('Total Hours Account')

# Show the plot
plt.show()

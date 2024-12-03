import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Reload the dataset
file_path = 'steam_user_games_data_filtered.csv'
data = pd.read_csv(file_path)


filtered_data = data[data['game_count'] < 500]

filtered_data['average_hours_per_game'] = (
    filtered_data['total_hours_played'] / filtered_data['game_count']
)

casuals = filtered_data[(filtered_data['game_count'] >= 26) & (filtered_data['game_count'] <= 50)]
normies = filtered_data[(filtered_data['game_count'] >= 1) & (filtered_data['game_count'] <= 25)]
gamers = filtered_data[filtered_data['game_count'] > 50]

def add_trendline(x, y, color):
    z = np.polyfit(x, y, 1)  # Fit a linear trendline
    p = np.poly1d(z)
    plt.plot(x, p(x), linestyle='--', color=color, label='Trendline')

plt.figure(figsize=(8, 5))
plt.scatter(casuals['game_count'], casuals['average_hours_per_game'], alpha=0.6, color='blue', label='Casuals', marker='o')
add_trendline(casuals['game_count'], casuals['average_hours_per_game'], 'blue')
plt.title('Casuals: Average Hours Per Game vs. Number of Games Owned')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.grid(True)
plt.legend()
plt.show()

# Scatter plot with trendline for Normies
plt.figure(figsize=(8, 5))
plt.scatter(normies['game_count'], normies['average_hours_per_game'], alpha=0.6, color='green', label='Normies', marker='o')
add_trendline(normies['game_count'], normies['average_hours_per_game'], 'green')
plt.title('Normies: Average Hours Per Game vs. Number of Games Owned')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.grid(True)
plt.legend()
plt.show()

# Scatter plot with trendline for Gamers
plt.figure(figsize=(8, 5))
plt.scatter(gamers['game_count'], gamers['average_hours_per_game'], alpha=0.6, color='red', label='Gamers', marker='o')
add_trendline(gamers['game_count'], gamers['average_hours_per_game'], 'red')
plt.title('Gamers: Average Hours Per Game vs. Number of Games Owned')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.grid(True)
plt.legend()
plt.show()

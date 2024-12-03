import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('steam_user_games_data_filtered.csv')

data.loc[:, 'percentage'] = (data['total_hours_played'] / data['game_count']) * 100

normies = data[(data['game_count'] >= 1) & (data['game_count'] <= 25)]
casuals = data[(data['game_count'] >= 26) & (data['game_count'] <= 50)]
gamers = data[data['game_count'] > 50]

mean_percentages = [
    normies['percentage'].mean() / 100,
    casuals['percentage'].mean() / 100,
    gamers['percentage'].mean() / 100
]

median_percentages = [
    normies['percentage'].median() / 100,
    casuals['percentage'].median() / 100,
    gamers['percentage'].median() / 100
]

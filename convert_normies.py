import os
from dotenv import load_dotenv
from steam_web_api import Steam
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the environment variables from the .env file
load_dotenv()

# Access the API key
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

with open("normies_random.txt", "r") as f:
    ids = [line.strip() for line in f if line.strip()]

data = []
for id in ids:
    try:
        response = steam.users.get_owned_games(id)
        if 'games' in response and response['games']:
            games_df = pd.DataFrame(response['games'])
            game_count = games_df.shape[0]
            # adding all the minutes played and converting to hours
            total_hours_played = games_df['playtime_forever'].sum() / 60  
            max_playtime = games_df['playtime_forever'].max()      
            # had to add a check since some players have not played within the 2 week span
            if 'playtime_2weeks' in games_df.columns:
                games_df['playtime_2weeks'] = games_df['playtime_2weeks'].sum() 
            else: 
                games_df['playtime_2weeks'] = 0  # if no 'playtime_2weeks'

            # get the max playtime and find the most played game(s)
            most_played_games = games_df[games_df['playtime_forever'] == max_playtime]['name'].tolist()
            # join the most played games list into a string, to handle ties
            most_played_res = ', '.join(most_played_games)
            

            # renaming columns for consistency
            games_df['steam_id'] = id
            games_df['game_count'] = game_count
            games_df['total_hours_account'] = round(total_hours_played, 2)
            games_df['most_played_game'] = most_played_res

            # Use consistent column names
            games_df = games_df.rename(columns={'total_hours_account': 'total_hours_account (hrs)', 'playtime_2weeks': 'playtime_2weeks (mins)'})

            data.append(games_df[['steam_id', 'game_count', 'total_hours_account (hrs)', 'most_played_game', 'name', 'playtime_forever', 'playtime_2weeks (mins)']])
            # print(games_df) 
        else:
            data.append(pd.DataFrame([{
            'steam_id': id,
            'game_count': 0,
            'total_hours_account (hrs)': 0,
            'most_played_game': [],
            'name': None,
            'playtime_forever (mins)': 0.0,
            'playtime_2weeks (mins)': 0.0
        }]))
            print(f"No games found for Steam ID {id}")
    except Exception as e:
        print(f"Error processing Steam ID {id}: {e}")

# group the data and dump as CSV file
res = pd.concat(data, ignore_index=True)
res.rename(columns={'name': 'game_name'}, inplace=True)
res.to_csv("steam_user_games_data_normies.csv", index=False)

# Top 10 most played games by total hours
most_played = res.groupby('game_name')['playtime_forever'].sum().nlargest(10)

# Plotting the top 10 games
plt.figure(figsize=(12, 8))
sns.barplot(x=most_played.values, y=most_played.index, palette="viridis")
plt.title("Top 10 Most Played Games by Total Hours (Normie Gamers)")
plt.xlabel("Total Hours Played")
plt.ylabel("Game Title")
plt.ticklabel_format(style='plain', axis='x')

plt.show()
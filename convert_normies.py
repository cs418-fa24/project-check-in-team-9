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
            total_hours_played = games_df['playtime_forever'].sum() / 60  
            game_names = games_df['name'].tolist() if 'name' in games_df.columns else []
            # had to add a check since some players have not played within the 2 week span
            if 'playtime_2weeks' in games_df.columns:
                games_df['playtime_2weeks'] = games_df['playtime_2weeks'].sum() / 60  
            else: 
                games_df['playtime_2weeks'] = 0  # if no 'playtime_2weeks'

            games_df['steam_id'] = id
            games_df['game_count'] = game_count
            games_df['total_hours_account'] = round(total_hours_played, 2)
            games_df['game_names'] = [game_names] * game_count  
            
            data.append(games_df[['steam_id', 'game_count', 'total_hours_account', 'game_names', 'name','playtime_2weeks']])
            # print(games_df) 
        else:
            data.append(pd.DataFrame([{
            'steam_id': id,
            'game_count': 0,
            'total_hours_account': 0.0,
            'game_names': [],
            'name': None,
            'playtime_forever': 0,
            'playtime_2weeks': 0.0
        }]))
            print(f"No games found for Steam ID {id}")
    except Exception as e:
        print(f"Error processing Steam ID {id}: {e}")

res = pd.concat(data, ignore_index=True)
res.rename(columns={'name': 'game_name'}, inplace=True)
res.to_csv("steam_user_games_data_normies.csv", index=False)

game_name = res.groupby('game_name')['playtime_2weeks'].sum().nlargest(10)
# Top 10
plt.figure(figsize=(12, 8))
sns.barplot(x=game_name.values, y=game_name.index, palette="viridis")
plt.title("Top 10 Most Played Games by Total Hours (Normie Gamers)")
plt.xlabel("Total Hours Played")
plt.ylabel("Game Title")
plt.show()

import os
import pandas as pd
from dotenv import load_dotenv
from steam_web_api import Steam
import matplotlib.pyplot as plt
import seaborn as sns

# Load environment variables
load_dotenv()
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)


with open("normies_random.txt", "r") as f:
    steam_ids = [line.strip() for line in f if line.strip()]


all_games_data = []


for steam_id in steam_ids:
    try:
        
        response = steam.users.get_owned_games(steam_id)
        

        if 'games' in response and response['games']:
            games_df = pd.DataFrame(response['games'])
            
            # Calculate game count and total hours played for the user
            game_count = games_df.shape[0]
            total_hours_played = games_df['playtime_forever'].sum() / 60  
            game_names = games_df['name'].tolist() if 'name' in games_df.columns else []
            
         
            games_df['steam_id'] = steam_id
            games_df['game_count'] = game_count
            games_df['total_hours_played'] = total_hours_played
            games_df['game_names'] = [game_names] * game_count  
            games_df['playtime_hours'] = games_df['playtime_forever'] / 60  
            
           
            all_games_data.append(games_df[['steam_id', 'game_count', 'total_hours_played', 'game_names', 'name', 'playtime_forever', 'playtime_hours']])
        else:
 
            all_games_data.append(pd.DataFrame([{
                'steam_id': steam_id,
                'game_count': 0,
                'total_hours_played': 0.0,
                'game_names': [],
                'name': None,
                'playtime_forever': 0,
                'playtime_hours': 0.0
            }]))
            print(f"No games found for Steam ID {steam_id}")
    except Exception as e:
        print(f"Error processing Steam ID {steam_id}: {e}")


all_games_df = pd.concat(all_games_data, ignore_index=True)


all_games_df.rename(columns={'name': 'most_played_game'}, inplace=True)

all_games_df.to_csv("steam_user_games_data.csv", index=False)


print("Data saved to steam_user_games_data.csv")


most_played_games = all_games_df.groupby('most_played_game')['playtime_hours'].sum().nlargest(10)

# Top 10
plt.figure(figsize=(12, 8))
sns.barplot(x=most_played_games.values, y=most_played_games.index, palette="viridis")
plt.title("Top 10 Most Played Games by Total Hours (Casual Gamers)")
plt.xlabel("Total Hours Played")
plt.ylabel("Game Title")
plt.show()

import os
import pandas as pd
from dotenv import load_dotenv
from steam_web_api import Steam


load_dotenv()

# Access the API key
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

# Search for the user and print the response structure
# response = steam.users.search_user("mmohaupt")
# print(response) 

# medf = pd.DataFrame.from_dict(response)

# print(medf.columns)

# if 'steamid' in medf.columns:
#     steamid = medf['steamid'][0]
#     gamer = steam.users.get_owned_games(steamid)
#     gamerdf = pd.DataFrame.from_dict(gamer)

#     if not gamerdf.empty:
#         print(gamerdf['game_count'][0])
#     else:
#         print("No games found.")
# else:
#     print("steamid not found in response.")

gamer = steam.users.get_owned_games(76561197960288464)
gamerdf = pd.DataFrame.from_dict(gamer)
print(gamerdf['game_count'][0])

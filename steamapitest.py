import os
import pandas as pd
from dotenv import load_dotenv
from steam_web_api import Steam

# Load the environment variables from the .env file
load_dotenv()

# Access the API key
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

response = steam.users.search_user("mmohaupt")
medf = pd.DataFrame.from_dict(response)
#76561198284996299     mmohaupt steamid
#76561197960288018     empty dataframe steamid
#76561197960298195     not real steam id
gamer = steam.users.get_owned_games(76561197960288018)
gamerdf = pd.DataFrame.from_dict(gamer)
# print(medf)
if(not gamerdf.empty):
    print(gamerdf['game_count'][0])
else:
    print("None")
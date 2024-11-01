import os
import pandas as pd
from dotenv import load_dotenv
from steam_web_api import Steam

# Load the environment variables from the .env file
load_dotenv()

# Access the API key
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

response = steam.users.search_user("sacredfighter8")
medf = pd.DataFrame.from_dict(response)
gamer = steam.users.get_owned_games(medf['player']['steamid'])
gamerdf = pd.DataFrame.from_dict(gamer)
# print(medf)
print(gamerdf['game_count'][0])
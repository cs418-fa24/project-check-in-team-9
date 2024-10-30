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
df = pd.DataFrame.from_dict(response)
print(df)
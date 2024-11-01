import os
import pandas as pd
from dotenv import load_dotenv
from steam_web_api import Steam

# Load the environment variables from the .env file
load_dotenv()

# Access the API key
KEY = os.getenv("STEAM_API_KEY")
steam = Steam(KEY)

# Steam IDs start with 765611, so this is the starting part of each ID.
starting = 765611
lowerbound = 97960287930  # Gabe Newell's ID, as low as the ID can go
#lowerbound = 7960288914
upperbound = 99000000000  # High bound for Steam IDs (for now)

# Open the output files once for efficient writing
with open("gamer.txt", "w") as gamer_file, open("casual.txt", "w") as casual_file, open("normie.txt", "w") as normie_file:
    
    # Loop through the range of potential Steam IDs
    for index in range(upperbound - lowerbound):
        gamesowned = -1
        tryid = int(str(starting) + str(lowerbound + index))  # Make a hypothetical Steam ID
        
        try:
            # Retrieve the number of owned games for the ID
            gamerid = steam.users.get_owned_games(tryid)
            gamerdf = pd.DataFrame.from_dict(gamerid)
            gamesowned = gamerdf['game_count'][0]
            
            # Check the game count and write to the appropriate file
            if gamesowned is not None:
                if gamesowned > 50:
                    gamer_file.write(f"{tryid}\n")
                elif gamesowned > 25:
                    casual_file.write(f"{tryid}\n")
                elif gamesowned > 0:
                    normie_file.write(f"{tryid}\n")
        except Exception as e:
            print(f"{tryid} is not a real ID: {e}")
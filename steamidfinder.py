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
#lowerbound = 97960287930  # Gabe Newell's ID, as low as the ID can go
#lowerbound = 98284996299 #mmohaupt id, just for testing
upperbound = 99000000000  # High bound for Steam IDs (for now)
#lowerbound = 97960298866 # last id check by matthew mohaupt 11/2/24 5:50pm

# Open the output files once for efficient writing
with open("gamer.txt", "a") as gamer_file, open("casual.txt", "a") as casual_file, open("normie.txt", "a") as normie_file:
    
    # Loop through the range of potential Steam IDs
    for index in range(upperbound - lowerbound):
        gamesowned = -1
        tryid = int(str(starting) + str(lowerbound + index))  # Make a hypothetical Steam ID
        
        try:
            # Retrieve the number of owned games for the ID
            gamerid = steam.users.get_owned_games(tryid)
            gamerdf = pd.DataFrame.from_dict(gamerid)
            
            # Check the game count and write to the appropriate file
            if(not gamerdf.empty):
                gamesowned = gamerdf['game_count'][0]
                print(f"{tryid} is definetly absolutly positively a real ID ")
                if gamesowned > 50:
                    gamer_file.write(f"{tryid}\n")
                elif gamesowned > 25:
                    casual_file.write(f"{tryid}\n")
                elif gamesowned > 0:
                    normie_file.write(f"{tryid}\n")
            else:
                print(f"{tryid} empty dataframe")
        except Exception as e:
            # Check if it's a "429 Too Many Requests" error
            if "429" in str(e):
                print(f"429 Too Many Requests error at index {index}. Last tested ID: {tryid}")
                break
            print(f"{tryid} is not a real ID: {e}")
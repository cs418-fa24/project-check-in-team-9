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
#upperbound = 99000000000  # High bound for Steam IDs (for now)
upperbound = 97960313167 # because i messed up in my data collection
#lowerbound = 97960298866 # last id check by matthew mohaupt 11/2/24 5:50pm
#lowerbound = 97960321657 #last id check by matthew mohaupt 11/2/24 idk when maybe at around 7pm
#lowerbound = 97960296149 #last id check by matthew mohaupt 11/3/24 12:55am
#lowerbound = 97960301151 #last id check by matthew mohaupt 11/3/24 4:41pm
lowerbound = 97960309675 #last id check by matthew mohaupt 11/3/24 8:59pm

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
            if(gamesowned > 0):
                print(f"{tryid} is definetly absolutly positively a real ID with number of games = {gamesowned}")
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
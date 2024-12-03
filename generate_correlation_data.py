import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

import os
from dotenv import load_dotenv

#dont hard code api keys, bad practice
load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")

# Function to fetch owned games
def get_owned_games(steam_id):
    try:
        response = requests.get(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/",
            params={
                "key": API_KEY,
                "steamid": steam_id,
                "include_appinfo": True,
                "format": "json"
            },
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error for Steam ID {steam_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching games for Steam ID {steam_id}: {e}")
        return None

# Function to categorize gamers
def categorize_gamers(game_count):
    if game_count <= 10:
        return "Casual"
    elif 10 < game_count <= 50:
        return "Normie"
    else:
        return "Gamer"

# Load Steam IDs
categories = ["casuals_random.txt", "normies_random.txt", "gamers_random.txt"]
all_games_data = []

for category in categories:
    with open(category, "r") as f:
        steam_ids = [line.strip() for line in f if line.strip()]

    # Process each Steam ID
    for steam_id in steam_ids:
        print(f"Processing Steam ID: {steam_id}")
        response = get_owned_games(steam_id)
        time.sleep(1)  # Add delay to avoid hitting API rate limits

        if response and "response" in response and "games" in response["response"]:
            games = response["response"]["games"]
            games_df = pd.DataFrame(games)

            if not games_df.empty:
                game_count = games_df.shape[0]
                total_hours_played = games_df["playtime_forever"].sum() / 60
                category_name = categorize_gamers(game_count)

                games_df["steam_id"] = steam_id
                games_df["game_count"] = game_count
                games_df["total_hours_played"] = total_hours_played
                games_df["category"] = category_name
                games_df["playtime_hours"] = games_df["playtime_forever"] / 60
                games_df["game_name"] = games_df["name"]  # Ensure meaningful names

                # Find the most played game
                games_df["most_played_game"] = games_df.loc[
                    games_df["playtime_hours"].idxmax(), "name"
                ] if "name" in games_df.columns else "Unknown"

                all_games_data.append(
                    games_df[
                        [
                            "steam_id",
                            "game_count",
                            "total_hours_played",
                            "category",
                            "most_played_game",
                            "game_name",
                            "playtime_hours",
                        ]
                    ]
                )
        else:
            print(f"No data received or no games found for Steam ID {steam_id}")

# Combine data into a single DataFrame
if all_games_data:
    all_games_df = pd.concat(all_games_data, ignore_index=True)

    # Filter out rows with non-positive total hours played
    all_games_df = all_games_df[all_games_df["total_hours_played"] > 0]

    # Remove outliers for total hours played (top 5%)
    total_hours_threshold = all_games_df["total_hours_played"].quantile(0.95)
    all_games_df = all_games_df[all_games_df["total_hours_played"] <= total_hours_threshold]

    # Remove outliers for game count (top 5%)
    game_count_threshold = all_games_df["game_count"].quantile(0.95)
    all_games_df = all_games_df[all_games_df["game_count"] <= game_count_threshold]

    all_games_df.drop_duplicates(subset=["steam_id"], inplace=True)
    all_games_df.to_csv("steam_user_games_data_filtered.csv", index=False)
    print("Filtered data saved to steam_user_games_data_filtered.csv")

    # Find the most played game in each category
    most_played_by_category = (
        all_games_df.groupby("category").apply(
            lambda x: x.loc[x["playtime_hours"].idxmax()][["most_played_game", "playtime_hours"]]
        )
    )

    # Reset index for easier plotting
    most_played_by_category.reset_index(drop=True, inplace=True)

    # Visualization: Most played game in each category
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        most_played_by_category["most_played_game"],
        most_played_by_category["playtime_hours"],
        color=["orange", "green", "blue"]
    )

    # Add labels and title
    plt.title("Most Played Game in Each Category (Filtered Data)")
    plt.xlabel("Game Title")
    plt.ylabel("Total Hours Played")
    plt.xticks(rotation=45, ha="right")

    # Add legend
    plt.legend(bars, most_played_by_category["most_played_game"], title="Categories", loc="upper right")

    plt.tight_layout()
    plt.show()

    print("Most played games by category:")
    print(most_played_by_category)
else:
    print("No valid data to process.")

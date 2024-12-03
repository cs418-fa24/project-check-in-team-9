import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data_path = "steam_user_games_data_filtered.csv"  
df = pd.read_csv(data_path)


df = df[df["total_hours_played"] > 0]


total_hours_threshold = df["total_hours_played"].quantile(0.95)
df = df[df["total_hours_played"] <= total_hours_threshold]


game_count_threshold = df["game_count"].quantile(0.95)
df = df[df["game_count"] <= game_count_threshold]


categories = df["category"].unique()
colors = ["green", "blue", "orange"]


plt.figure(figsize=(12, 8))

for i, category in enumerate(categories):
    subset = df[df["category"] == category]
    plt.scatter(
        subset["game_count"],
        subset["total_hours_played"],
        color=colors[i],
        alpha=0.7,
        label=f"{category} Data Points"
    )

z = np.polyfit(df["game_count"], df["total_hours_played"], 1)
p = np.poly1d(z)
x_range = np.linspace(df["game_count"].min(), df["game_count"].max(), 500)
plt.plot(
    x_range,
    p(x_range),
    color="red",
    label="Overall Trendline"
)

plt.title("Correlation Between Number of Games Owned and Total Playtime by Category (No Outliers)")
plt.xlabel("Number of Games Owned")
plt.ylabel("Total Hours Played")
plt.ylim(bottom=0)  
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()

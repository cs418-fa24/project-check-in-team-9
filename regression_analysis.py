import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the data
data = pd.read_csv('steam_user_games_data_filtered.csv')

# Calculate average hours per game
data['avg_hours_per_game'] = data['total_hours_played'] / data['game_count']

# Remove outliers (average hours per game > 400 and game count > 500)
filtered_data = data[data['avg_hours_per_game'] <= 400]
filtered_data = filtered_data[filtered_data['game_count'] <= 500]

# Prepare the data for regression: `game_count` vs `avg_hours_per_game`
X_avg = filtered_data[['game_count']]
y_avg = filtered_data['avg_hours_per_game']

# Fit the linear regression model for average hours per game
model_avg = LinearRegression()
model_avg.fit(X_avg, y_avg)

# Predictions using the updated regression model
predicted_y_avg = model_avg.predict(X_avg)

# Regression coefficients for average hours per game
slope_avg = model_avg.coef_[0]
intercept_avg = model_avg.intercept_

# Visualization for average hours per game with categories
categories = filtered_data['category'].unique()
plt.figure(figsize=(12, 8))
colors = {'Normie': 'blue', 'Casual': 'green', 'Gamer': 'red'}

for category in categories:
    subset = filtered_data[filtered_data['category'] == category]
    plt.scatter(
        subset['game_count'],
        subset['avg_hours_per_game'],
        color=colors[category],
        alpha=0.6,
        label=category,
        edgecolor='black'
    )

# Plot regression line
plt.plot(X_avg, predicted_y_avg, color='orange', linewidth=2, label='Regression Line')
plt.title('Linear Regression: Game Count vs Average Hours Per Game')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.legend(title='Categories')
plt.grid()
plt.show()

# R-squared calculation for the updated model
r_squared_avg = model_avg.score(X_avg, y_avg)

# Display results
print("Slope:", slope_avg)
print("Intercept:", intercept_avg)
print("R-squared:", r_squared_avg)

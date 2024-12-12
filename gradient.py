import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv("steam_user_games_data_filtered.csv")

# Ensure no division by zero
data['avg_hours_per_game'] = data['total_hours_played'] / data['game_count'].replace(0, float('nan'))
data.dropna(subset=['avg_hours_per_game'], inplace=True)

# Remove outliers
filtered_data = data[(data['avg_hours_per_game'] <= 400) & (data['game_count'] <= 500)]

# Prepare the data
X = filtered_data[['game_count']]
y = filtered_data['avg_hours_per_game']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Gradient Boosting Regressor
gbr = GradientBoostingRegressor(random_state=42)
gbr.fit(X_train, y_train)
y_pred_gbr = gbr.predict(X_test)

# Evaluate the model
mse_gbr = mean_squared_error(y_test, y_pred_gbr)
r2_gbr = r2_score(y_test, y_pred_gbr)
print(f"Gradient Boosting Regressor - MSE: {mse_gbr}, R-squared: {r2_gbr}")

# Visualization: Gradient Boosting
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual', alpha=0.6, edgecolor='black', marker='o')
plt.scatter(X_test, y_pred_gbr, color='purple', label='Predicted (Gradient Boosting)', alpha=0.6, edgecolor='black', marker='o')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.title('Gradient Boosting: Predicted vs Actual')
plt.legend()
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()
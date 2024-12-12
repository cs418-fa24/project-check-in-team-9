from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load and preprocess the data
file_path = 'steam_user_games_data_filtered.csv'
data = pd.read_csv(file_path)


filtered_data = data[data['game_count'] < 500]
filtered_data['average_hours_per_game'] = filtered_data['total_hours_played'] / filtered_data['game_count']



# Filter the data (removing outliers and invalid values)
filtered_data['Category'] = pd.cut(
    filtered_data['game_count'],
    bins=[0, 25, 50, float('inf')],
    labels=['Normie', 'Casual', 'Gamer']
)

# Encode the target variable
filtered_data['Category_encoded'] = filtered_data['Category'].cat.codes

# Prepare the data
X = filtered_data[['game_count', 'average_hours_per_game']].dropna()
y = filtered_data['Category_encoded']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

# Plot decision boundary (if needed)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_test['game_count'], y=X_test['average_hours_per_game'], hue=y_pred, palette='Set1')
plt.title('Classification Results for Gaming Behavior')
plt.xlabel('Number of Games Owned')
plt.ylabel('Average Hours Per Game')
plt.show()
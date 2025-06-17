from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

# Sample data for training (simulate different scenarios)
data = pd.DataFrame({
    'latitude': [13.0, 13.01, 13.05, 13.1, 13.2, 13.25],
    'longitude': [75.0, 75.02, 75.05, 75.1, 75.2, 75.25],
    'distance_to_forest_center': [100, 500, 1500, 3000, 4000, 100],
    'distance_to_leopard': [100, 200, 500, 700, 1500, 50],
    'time_of_day': [0, 1, 2, 1, 3, 2],  # Encoded (0: morning, 1: afternoon, etc.)
    'risk_level': [2, 2, 1, 1, 0, 2]  # Target: 0 = low, 1 = medium, 2 = high
})

# Features and label
X = data.drop(columns='risk_level')
y = data['risk_level']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "risk_predictor_model.pkl")

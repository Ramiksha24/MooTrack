import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ---------------------------
# Step 1: Generate Dataset
# ---------------------------

def generate_synthetic_data(n=300):
    data = []
    time_options = ['morning', 'afternoon', 'evening', 'night']

    for _ in range(n):
        distance_to_forest = np.random.uniform(50, 1000)
        distance_to_leopard = np.random.uniform(0, 1000)
        time_of_day = np.random.choice(time_options)

        # Risk Logic
        if distance_to_leopard < 50:
            risk = 'very high'
        elif distance_to_leopard < 100:
            risk = 'high'
        elif distance_to_leopard < 300:
            risk = 'medium'
        else:
            risk = 'low'

        data.append({
            'distance_to_forest': round(distance_to_forest, 2),
            'distance_to_leopard': round(distance_to_leopard, 2),
            'time_of_day': time_of_day,
            'risk_level': risk
        })

    return pd.DataFrame(data)

df = generate_synthetic_data()

# ---------------------------
# Step 2: Encode + Split
# ---------------------------

X = df[['distance_to_forest', 'distance_to_leopard', 'time_of_day']]
y = df['risk_level']

# Encode time_of_day
time_encoder = LabelEncoder()
X['time_of_day'] = time_encoder.fit_transform(X['time_of_day'])

# Save the encoder for inference
joblib.dump(time_encoder, "time_of_day_encoder.pkl")

# ---------------------------
# Step 3: Train ML Model
# ---------------------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict on training set
y_pred = model.predict(X)

# ---------------------------
# Step 4: Evaluate
# ---------------------------

print("\n🎯 Accuracy:", accuracy_score(y, y_pred))
print("\n📊 Classification Report:\n")
print(classification_report(y, y_pred))

# ---------------------------
# Step 5: Save the model
# ---------------------------

joblib.dump(model, "risk_predictor_model.pkl")

# ---------------------------
# Optional: Save dataset
# ---------------------------

df.to_csv("mootrack_risk_dataset.csv", index=False)
print("\n✅ Model and dataset saved.")

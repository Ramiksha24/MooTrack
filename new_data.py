import pandas as pd
import numpy as np
import random

# Helper function
def generate_risk(dist_leo, dist_forest, time_of_day):
    if dist_leo < 300:
        if time_of_day in [2, 3]:  # Evening or Night
            return 2  # HIGH
        else:
            return 1  # MEDIUM
    elif dist_forest < 200:
        if time_of_day == 3:  # Night
            return 1  # MEDIUM
        else:
            return 0  # LOW
    else:
        return 0  # LOW

# Generate synthetic data
data = []
time_map = {0: "morning", 1: "afternoon", 2: "evening", 3: "night"}

for i in range(1000):
    cow_id = f"COW{str(random.randint(1, 10)).zfill(3)}"
    dist_to_leo = round(np.random.uniform(0, 1000), 2)
    dist_to_forest = round(np.random.uniform(0, 1000), 2)
    time_of_day = random.randint(0, 3)  # encoded as integer
    risk = generate_risk(dist_to_leo, dist_to_forest, time_of_day)

    data.append([cow_id, dist_to_leo, dist_to_forest, time_of_day, risk])

df = pd.DataFrame(data, columns=[
    "cow_id",
    "distance_to_leopard",
    "distance_to_forest",
    "time_of_day",
    "risk_level"
])

# Save to CSV
df.to_csv("synthetic_cow_risk_data.csv", index=False)
print("✅ Dataset generated and saved as 'synthetic_cow_risk_data.csv'")

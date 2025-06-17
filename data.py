import pandas as pd
from pymongo import MongoClient

# Load CSV
df = pd.read_csv("cow_leopard_data.csv")

# Connect to MongoDB
client = MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/mootrack")
db = client["mootrack"]
collection = db["cow_risk_data"]

# Convert rows to dict and insert
records = df.to_dict(orient='records')
collection.insert_many(records)

print("✅ Data imported to MongoDB successfully.")

import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/mootrack")
db = client["mootrack"]
collection = db["cow_risk_data"]

# Load data into DataFrame
data = pd.DataFrame(list(collection.find()))

# Drop MongoDB internal ID
data.drop(columns=['_id'], inplace=True)
print(data.head())

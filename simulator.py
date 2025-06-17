# simulator.py
import pymongo
import random
import time
from datetime import datetime

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/?retryWrites=true&w=majority&appName=mootrack")
db = client["mootrack"]
cow_locations = db["cow_locations"]

# Base location (somewhere safe-ish)
base_lat, base_lon = 13.6350, 74.8450

while True:
    for i in range(10):
        cow_id = f"COW{i+1:03d}"
        # Random movement around base
        lat = base_lat + random.uniform(-0.002, 0.002)
        lon = base_lon + random.uniform(-0.002, 0.002)

        # Save to MongoDB
        cow_locations.insert_one({
            "cow_id": cow_id,
            "location": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "timestamp": datetime.utcnow()
        })

    print("✅ Updated cow locations.")
    time.sleep(5)  # update every 5 seconds

import pymongo
import random
import time
from geopy.distance import geodesic
from math import cos, sin, pi

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/?retryWrites=true&w=majority&appName=mootrack")
db = client["mootrack"]
db = client["mootrack"]
cow_locations = db["cow_locations"]

# Leopard location (simulate one fixed point)
leopard_lat = 13.6355
leopard_lon = 74.8445
leopard_coord = (leopard_lat, leopard_lon)

cow_locations.delete_many({})  # Clean slate

def generate_cow_coord(risk_level):
    """Generate coordinates based on desired risk level."""
    angle = random.uniform(0, 2 * pi)

    if risk_level == "high":
        distance = random.uniform(10, 100)  # meters
    elif risk_level == "medium":
        distance = random.uniform(100, 300)
    else:
        distance = random.uniform(300, 700)

    # Approximate conversion (1 degree ~ 111111m)
    offset = distance / 111111

    lat = leopard_lat + offset * cos(angle)
    lon = leopard_lon + offset * sin(angle)

    return lat, lon

while True:
    print("🔄 Updating cow positions...")

    cow_locations.delete_many({})

    for i in range(10):
        if i < 3:
            risk = "high"
        elif i < 6:
            risk = "medium"
        else:
            risk = "low"

        lat, lon = generate_cow_coord(risk)

        cow_locations.insert_one({
            "cow_id": f"COW{i+1:03d}",
            "location": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "timestamp": time.time()
        })

    print("✅ Cow positions updated.")
    time.sleep(10)

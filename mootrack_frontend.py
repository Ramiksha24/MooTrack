import streamlit as st
from streamlit_folium import st_folium
import folium
import pymongo
import time
from geopy.distance import geodesic
import joblib
import numpy as np
from datetime import datetime

# -----------------------
# Load ML Model + Encoder
# -----------------------
try:
    model = joblib.load("D:/mootrack/risk_predictor_model.pkl")
    encoder = joblib.load("D:/mootrack/time_of_day_encoder.pkl")
    model_loaded = True
except:
    st.error("🚫 ML model or encoder not found. Please train the model first.")
    model_loaded = False

# -----------------------
# MongoDB Connection
# -----------------------
client = pymongo.MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/?retryWrites=true&w=majority&appName=mootrack")
db = client["mootrack"]
cow_locations = db["cow_locations"]
leopard_sightings = db["leopard_sightings"]
forest_zones = db["forest_zones"]

# -----------------------
# Helper Functions
# -----------------------
def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 20:
        return 'evening'
    else:
        return 'night'

def predict_risk(dist_forest, dist_leopard, time_of_day):
    time_encoded = encoder.transform([time_of_day])[0]
    X = np.array([[dist_forest, dist_leopard, time_encoded]])
    prediction = model.predict(X)[0]
    return prediction

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config
st.title("🐄 MooTrack Dashboard")
st.markdown("Real-time Cow Tracking + AI Leopard Risk Prediction")

# Delay to prevent blinking
st.info("⏳ Updating every 10 seconds. This keeps your map smooth and data fresh.")
time.sleep(5)

# -----------------------
# Fetch Data from MongoDB
# -----------------------
cows = cow_locations.find().sort("timestamp", -1).limit(10)
leopards = list(leopard_sightings.find())
forest = forest_zones.find_one()

# -----------------------
# Draw Map
# -----------------------
if cows:
    # Center map on the first cow
    first = list(cows)[0]
    cow_lat, cow_lon = first["location"]["coordinates"][1], first["location"]["coordinates"][0]
    map_obj = folium.Map(location=[cow_lat, cow_lon], zoom_start=15)

    # Forest zone polygon
    if forest:
        forest_coords = [(pt[1], pt[0]) for pt in forest["area"]["coordinates"][0]]
        folium.Polygon(
            locations=forest_coords,
            color="green",
            fill=True,
            fill_opacity=0.2,
            tooltip="Forest Zone"
        ).add_to(map_obj)

    for cow in cow_locations.find().sort("timestamp", -1).limit(10):
        coords = cow["location"]["coordinates"]
        lat, lon = coords[1], coords[0]
        cow_id = cow.get("cow_id", "Unknown")

        # Distance to forest center
        if forest:
            poly_coords = forest["area"]["coordinates"][0]
            avg_lat = sum([pt[1] for pt in poly_coords]) / len(poly_coords)
            avg_lon = sum([pt[0] for pt in poly_coords]) / len(poly_coords)
            dist_to_forest = geodesic((lat, lon), (avg_lat, avg_lon)).meters
        else:
            dist_to_forest = 999

        # Distance to nearest leopard
        nearest_dist = 9999
        for leo in leopards:
            leo_lat = leo["location"]["coordinates"][1]
            leo_lon = leo["location"]["coordinates"][0]
            dist = geodesic((lat, lon), (leo_lat, leo_lon)).meters
            nearest_dist = min(nearest_dist, dist)

            # Add leopard marker
            folium.Marker(
                [leo_lat, leo_lon],
                icon=folium.Icon(color='red', icon='paw'),
                popup="🐆 Leopard"
            ).add_to(map_obj)

            # Danger zone
            folium.Circle(
                radius=300,
                location=[leo_lat, leo_lon],
                color="orange",
                fill=True,
                fill_opacity=0.1,
                popup="⚠️ Danger Zone (300m)"
            ).add_to(map_obj)

        # Predict risk
        risk = predict_risk(dist_to_forest, nearest_dist, get_time_of_day()) if model_loaded else "N/A"
        color = "red" if risk in ["high", "very high"] else "orange" if risk == "medium" else "green"

        # Cow marker
        folium.Marker(
            [lat, lon],
            popup=f"🐄 Cow ID: {cow_id}<br>📏 Forest: {dist_to_forest:.1f}m<br>🐆 Leopard: {nearest_dist:.1f}m<br>🧠 Risk: <b>{risk.upper()}</b>",
            icon=folium.Icon(color=color)
        ).add_to(map_obj)

    # Show map
    st_folium(map_obj, width=1000, height=600)

else:
    st.warning("No cow data found.")

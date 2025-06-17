
import streamlit as st
from streamlit_folium import st_folium
import folium
import pymongo
import datetime
import time
from geopy.distance import geodesic
import joblib

# Title
st.title("🐄 MooTrack Dashboard")
st.subheader("Live Cow Tracking and Leopard Alert System")

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/?retryWrites=true&w=majority&appName=mootrack")
db = client["mootrack"]
cow_locations = db["cow_locations"]
leopard_sightings = db["leopard_sightings"]
forest_zones = db["forest_zones"]

# Load the risk prediction model
@st.cache_resource
def load_model():
    return joblib.load("risk_predictor_model.pkl")

model = load_model()

# Risk color mapping
risk_colors = {
    "LOW": "blue",
    "MEDIUM": "orange",
    "HIGH": "red"
}

def predict_risk(dist_leopard, dist_forest):
    try:
        pred = model.predict([[dist_leopard, dist_forest]])
        return pred[0]
    except Exception as e:
        return "Error"

# Get the 10 most recent cow locations
cows = cow_locations.find().sort("timestamp", -1).limit(10)
cow_data = list(cows)

if cow_data:
    # Use the first cow to center the map
    center = cow_data[0]["location"]["coordinates"]
    center_lat, center_lon = center[1], center[0]
    map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # Load forest polygon
    forest = forest_zones.find_one()
    forest_poly = []
    if forest:
        forest_poly = [(pt[1], pt[0]) for pt in forest["area"]["coordinates"][0]]
        folium.Polygon(
            locations=forest_poly,
            color="green",
            fill=True,
            fill_opacity=0.3,
            tooltip="Forest Zone"
        ).add_to(map_obj)

    # Add leopard sightings
    leopard_coords = []
    for sighting in leopard_sightings.find():
        leo = sighting["location"]["coordinates"]
        leo_lat, leo_lon = leo[1], leo[0]
        leopard_coords.append((leo_lat, leo_lon))

        folium.Marker(
            [leo_lat, leo_lon],
            popup=f"🐆 Leopard",
            icon=folium.Icon(color="darkred", icon="exclamation-sign")
        ).add_to(map_obj)

        folium.Circle(
            radius=300,
            location=[leo_lat, leo_lon],
            color='orange',
            fill=True,
            fill_opacity=0.2
        ).add_to(map_obj)

    # Process each cow
    for cow in cow_data:
        cow_coord = cow["location"]["coordinates"]
        lat, lon = cow_coord[1], cow_coord[0]
        cow_id = cow["cow_id"]

        # Distance to closest leopard
        dist_to_leopard = min([geodesic((lat, lon), leo).meters for leo in leopard_coords], default=9999)

        # Distance to forest (center to nearest vertex)
        if forest_poly:
            dist_to_forest = min([geodesic((lat, lon), pt).meters for pt in forest_poly])
        else:
            dist_to_forest = 9999

        # Risk prediction
        risk = predict_risk(dist_to_leopard, dist_to_forest)
        color = risk_colors.get(risk, "gray")

        # Add marker with color based on risk
        folium.Marker(
            location=[lat, lon],
            popup=f"Cow {cow_id} | Risk: {risk}",
            icon=folium.Icon(color=color)
        ).add_to(map_obj)

        # Display info
        st.markdown(f"""
        ### 🐄 {cow_id}
        - 🌍 Location: ({lat:.5f}, {lon:.5f})
        - 🐆 Distance to Leopard: {dist_to_leopard:.1f}m
        - 🌲 Distance to Forest: {dist_to_forest:.1f}m
        - 🧠 **Predicted Risk Level:** :red[**{risk}**]
        ---
        """)

    # Show map
    st_folium(map_obj, width=700, height=500)

    # Auto-refresh every 5 seconds
    st.experimental_user()

else:
    st.warning("No cow data found.")

import streamlit as st
import os
st.set_page_config(layout="wide", page_title="MooTrack Dashboard")

from streamlit_folium import st_folium
import folium
import pymongo
import time
from geopy.distance import geodesic
import joblib
import numpy as np
from datetime import datetime

# -----------------------
# Configuration
# -----------------------
@st.cache_resource
def load_ml_model():
    """Load ML model and encoder with caching"""
    try:
        # Use relative paths
        model_path = "risk_predictor_model.pkl"
        encoder_path = "time_of_day_encoder.pkl"
        
        if not os.path.exists(model_path) or not os.path.exists(encoder_path):
            st.error("🚫 Model files not found. Please ensure model files are in the repository.")
            return None, None, False
            
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
        return model, encoder, True
    except Exception as e:
        st.error(f"🚫 Error loading ML model: {str(e)}")
        return None, None, False

@st.cache_resource
def init_mongodb():
    """Initialize MongoDB connection with caching"""
    try:
        # Use secrets for MongoDB connection
        if "mongo" in st.secrets:
            mongo_uri = st.secrets["mongo"]["connection_string"]
        else:
            # Fallback for local development
            mongo_uri = "mongodb+srv://RamikshaShetty:Rami%409632@mootrack.felumhi.mongodb.net/?retryWrites=true&w=majority&appName=mootrack"
            
        client = pymongo.MongoClient(mongo_uri)
        db = client["mootrack"]
        
        # Test connection
        client.admin.command('ping')
        return db, True
    except Exception as e:
        st.error(f"🚫 MongoDB connection failed: {str(e)}")
        return None, False

# Load resources
model, encoder, model_loaded = load_ml_model()
db, db_connected = init_mongodb()

if not db_connected:
    st.stop()

# Collections
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
    if not model_loaded:
        return "N/A"
    try:
        time_encoded = encoder.transform([time_of_day])[0]
        X = np.array([[dist_forest, dist_leopard, time_encoded]])
        prediction = model.predict(X)[0]
        return prediction
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return "Error"

# -----------------------
# Streamlit UI
# -----------------------
st.title("🐄 MooTrack Dashboard")
st.markdown("Real-time Cow Tracking + AI Leopard Risk Prediction")

# Status indicators
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("ML Model", "✅ Loaded" if model_loaded else "❌ Failed")
with col2:
    st.metric("Database", "✅ Connected" if db_connected else "❌ Disconnected")
with col3:
    current_time = get_time_of_day()
    st.metric("Time of Day", current_time.title())

# Auto-refresh
if st.button("🔄 Refresh Data"):
    st.cache_resource.clear()

# Rest of your mapping code here...
# (keeping the same logic but with error handling)

try:
    cows = list(cow_locations.find().sort("timestamp", -1).limit(10))
    leopards = list(leopard_sightings.find())
    forest = forest_zones.find_one()
    
    if cows:
        # Your existing mapping code here
        # ... (same as before but with better error handling)
        pass
    else:
        st.warning("📍 No cow location data found in database.")
        st.info("💡 Run the cow simulator to generate sample data.")
        
except Exception as e:
    st.error(f"❌ Error fetching data: {str(e)}")

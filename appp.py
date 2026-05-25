import streamlit as st
import random
import pandas as pd
import joblib
import time

# Load model
model = joblib.load("aqi_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Title
st.title("AI-Based Indoor Air Quality Monitoring System")

st.write("Real-Time Indoor Air Quality Prediction Dashboard")

# Store historical data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "PM2.5",
        "CO2",
        "VOC",
        "Temperature",
        "Humidity"
    ])

# Generate simulated sensor values
pm25 = random.randint(5, 180)
co2 = random.randint(350, 2000)
voc = random.randint(50, 500)
temp = random.randint(20, 38)
humidity = random.randint(30, 85)

# Display live sensor values
st.subheader("Live Sensor Data")

col1, col2 = st.columns(2)

with col1:
    st.metric("PM2.5", pm25)
    st.metric("CO2", co2)
    st.metric("VOC", voc)

with col2:
    st.metric("Temperature", temp)
    st.metric("Humidity", humidity)

# Create dataframe for prediction
new_data = pd.DataFrame([[
    pm25,
    co2,
    voc,
    temp,
    humidity
]], columns=[
    "PM2.5",
    "CO2",
    "VOC",
    "Temperature",
    "Humidity"
])

# Append to historical data
st.session_state.data = pd.concat([
    st.session_state.data,
    new_data
], ignore_index=True)

# Keep only latest 20 readings
st.session_state.data = st.session_state.data.tail(20)

# Predict AQI
prediction = model.predict(new_data)

# Convert prediction back to text
aqi = encoder.inverse_transform(prediction)

# Display AQI
# ------------------------
# AQI DISPLAY
# ------------------------

st.subheader("Predicted AQI")

# ------------------------
# AUTOMATIC LOGIC
# ------------------------

if aqi[0] == "Good":

    st.success("AQI Status: GOOD")

    purifier_status = "OFF"
    fan_speed = "LOW"

elif aqi[0] == "Moderate":

    st.warning("AQI Status: MODERATE")

    purifier_status = "OFF"
    fan_speed = "MEDIUM"

elif aqi[0] == "Poor":

    st.error("AQI Status: POOR")

    purifier_status = "ON"
    fan_speed = "HIGH"

else:

    st.error("AQI Status: HAZARDOUS")

    purifier_status = "ON"
    fan_speed = "MAXIMUM"

# ------------------------
# DISPLAY AUTOMATION STATUS
# ------------------------

st.subheader("Automatic Control System")

col1, col2 = st.columns(2)

with col1:
    st.metric("Purifier Status", purifier_status)

with col2:
    st.metric("Fan Speed", fan_speed)

# ------------------------
# ALERT SYSTEM
# ------------------------

st.subheader("Alert System")

if aqi[0] == "Good":

    st.success("Air Quality is Safe")

elif aqi[0] == "Moderate":

    st.warning("Air Quality Slightly Affected")

elif aqi[0] == "Poor":

    st.error("WARNING: Poor Air Quality Detected!")

    st.warning("Purifier Activated Automatically")

else:

    st.error("DANGER: Hazardous Air Quality!")

    st.error("Emergency Ventilation Activated!")

    st.warning("Avoid Staying Indoors for Long Duration")

# Purifier status
st.subheader("Purifier Status")

if aqi[0] in ["Poor", "Hazardous"]:
    st.error("Purifier ON")

else:
    st.success("Purifier OFF")

# ------------------------
# LIVE GRAPHS
# ------------------------

st.subheader("Real-Time Graphs")

# PM2.5 Graph
st.line_chart(st.session_state.data["PM2.5"])

# CO2 Graph
st.line_chart(st.session_state.data["CO2"])

# VOC Graph
st.line_chart(st.session_state.data["VOC"])

# Temperature & Humidity Graph
st.line_chart(
    st.session_state.data[[
        "Temperature",
        "Humidity"
    ]]
)

# Auto refresh
time.sleep(2)
st.rerun()
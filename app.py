import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load Saved Files
# -----------------------------
model = joblib.load("models/traffic_stress.pkl")
scaler = joblib.load("models/svr_scaler.pkl")
le1 = joblib.load("models/le1.pkl")
le2 = joblib.load("models/le2.pkl")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Urban Traffic Stress Predictor",
    page_icon="🚦",
    layout="centered"
)

st.title("🚦 Urban Traffic Stress Prediction")
st.write(
    "Predict the driver's stress level based on traffic and road conditions."
)

# -----------------------------
# User Inputs
# -----------------------------
traffic_density = st.slider(
    "Traffic Density (vehicles/km)",
    min_value=0,
    max_value=150,
    value=50
)

horn_events_per_min = st.slider(
    "Horn Events Per Minute",
    min_value=0,
    max_value=20,
    value=10
)

avg_speed = st.slider(
    "Average Speed (km/h)",
    min_value=0,
    max_value=120,
    value=40
)

signal_wait_time = st.slider(
    "Signal Wait Time (seconds)",
    min_value=0,
    max_value=90,
    value=30
)

weather_condition = st.selectbox(
    "Weather Condition",
    le1.classes_
)

road_quality_score = st.slider(
    "Road Quality Score",
    min_value=4,
    max_value=10,
    value=6
)

driver_experience_level = st.selectbox(
    "Driver Experience Level",
    le2.classes_
)
# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Stress Index"):

    weather_encoded = le1.transform([weather_condition])[0]
    driver_encoded = le2.transform([driver_experience_level])[0]

    input_data = pd.DataFrame(
        [[
            traffic_density,
            horn_events_per_min,
            avg_speed,
            signal_wait_time,
            weather_encoded,
            road_quality_score,
            driver_encoded
        ]],
        columns=[
            "traffic_density",
            "horn_events_per_min",
            "avg_speed",
            "signal_wait_time",
            "weather_condition",
            "road_quality_score",
            "driver_experience_level"
        ]
    )

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)[0]

    st.success(f"Predicted Stress Index: {prediction:.2f}")

    if prediction < 50:
        st.info("🟢 Low Stress")
    else:
        st.error("🔴 High Stress")
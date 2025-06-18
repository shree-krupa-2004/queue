import streamlit as st
import joblib
import pandas as pd
import os

st.title("🕒 Smart Queue Wait Time Predictor")

try:
    if not os.path.exists("queue_model.pkl"):
        st.error("queue_model.pkl not found! Please add it to your repository.")
    else:
        model = joblib.load("queue_model.pkl")

        # Inputs
        queue_length = st.slider("Queue Length", 1, 50, 10)
        hour = st.slider("Current Hour (24H)", 0, 23, 12)
        day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
        avg_time = st.number_input("Avg Service Time per Person (min)", min_value=1, max_value=10, value=5)

        # Create input dict with base features
        input_data = {
            "queue_length": queue_length,
            "avg_service_time": avg_time,
            "hour": hour,
        }

        # Add all day_of_week columns, set to 0
        for day_col in [
            "day_of_week_Friday", "day_of_week_Monday", "day_of_week_Saturday",
            "day_of_week_Sunday", "day_of_week_Thursday", "day_of_week_Tuesday", "day_of_week_Wednesday"
        ]:
            input_data[day_col] = 1 if f"day_of_week_{day}" == day_col else 0

        # Add all weather columns, set to 0
        for weather_col in ["weather_Cloudy", "weather_Rainy", "weather_Sunny"]:
            input_data[weather_col] = 1 if f"weather_{weather}" == weather_col else 0

        # All required columns in the correct order
        all_cols = [
            "queue_length", "avg_service_time", "hour",
            "day_of_week_Friday", "day_of_week_Monday", "day_of_week_Saturday",
            "day_of_week_Sunday", "day_of_week_Thursday", "day_of_week_Tuesday",
            "day_of_week_Wednesday", "weather_Cloudy", "weather_Rainy", "weather_Sunny"
        ]

        # Create DataFrame with columns in the correct order
        X_input = pd.DataFrame([[input_data[col] for col in all_cols]], columns=all_cols)

        # Predict
        prediction = model.predict(X_input)[0]

        st.success(f"⏳ Estimated Wait Time: **{prediction:.1f} minutes**")
except Exception as e:
    st.error(f"An error occurred: {e}")

import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("karnataka_corn_model.pkl")

# Title
st.title("🌽 ಮಕ್ಕಜೋಳ ಇಳುವರಿ ಮುನ್ಸೂಚನೆ | Maize Yield Predictor")

# Input layout
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("ಜಿಲ್ಲೆ | District",
                            ['Mandya', 'Haveri', 'Dharwad', 'Bangalore Rural'])
    tmax = st.slider("ಗರಿಷ್ಠ ತಾಪಮಾನ | Max Temp (°C)", 25, 45, 32)
    tmin = st.slider("ಕನಿಷ್ಠ ತಾಪಮಾನ | Min Temp (°C)", 15, 30, 22)

with col2:
    rain = st.slider("ಮಳೆಯ ಪ್ರಮಾಣ | Rainfall (mm)", 0, 1200, 700, step=10)
    humidity = st.slider("ಆದ್ರತೆ | Humidity (%)", 40, 100, 75)

# Feature calculations
gdd = max(0, min((tmin + tmax) / 2 - 10, 20))
cum_gdd = gdd * 100
rain_anom = rain - 700

# Soil values (static for now)
soil_ph, n, p, k, oc = 6.2, 120, 35, 55, 0.8

# Prepare input
input_data = [[
    tmax, tmin, rain, humidity,
    gdd, cum_gdd,
    soil_ph, n, p, k, oc,
    rain_anom
]]

# Predict yield
pred = model.predict(input_data)[0]

# Display results
st.success(f"Yield: {pred:.0f} kg/ha")
st.success(f"ಇಳುವರಿ: {pred:.0f} ಕೆ.ಜಿ/ಹೆಕ್ಟೇರ್")

# Dynamic alert based on yield
if pred < 4500:
    st.warning("⚠ ಕಡಿಮೆ ಇಳುವರಿ ಸಾಧ್ಯತೆ | Low yield expected")
elif pred < 5000:
    st.info("🟡 ಮಧ್ಯಮ ಇಳುವರಿ ಸಾಧ್ಯತೆ | Moderate yield expected")
else:
    st.success("✅ ಉತ್ತಮ ಬೆಳೆಯ ಸಾಧ್ಯತೆ | Good crop potential")

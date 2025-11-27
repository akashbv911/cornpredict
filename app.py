import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("karnataka_corn_model.pkl")

st.title("ಮೆಕ್ಕೆ ಜೋಳ ಇಳುವರಿ ಮುನ್ಸೂಚನೆ | Maize Yield Predictor")

col1, col2 = st.columns(2)
with col1:
    district = st.selectbox("ಜಿಲ್ಲೆ | District", ['Mandya', 'Haveri', 'Dharwad', 'Bangalore Rural'])
    tmax = st.slider("ಗರಿಷ್ಠ ತಾಪಮಾನ | Max Temp (°C)", 25, 40, 32)
    tmin = st.slider("ಕನಿಷ್ಠ ತಾಪಮಾನ | Min Temp (°C)", 18, 28, 22)
with col2:
    rain = st.slider("ಮಳೆ | Rainfall (mm)", 400, 1200, 700)
    humidity = st.slider("ತೇವಾಂಶ | Humidity (%)", 60, 90, 75)

# Dummy values
gdd = max(0, min((tmin + tmax)/2 - 10, 20))
cum_gdd = gdd * 100
rain_anom = rain - 700
soil_ph, n, p, k, oc = 6.2, 120, 35, 55, 0.8

input_data = [[tmax, tmin, rain, humidity, gdd, cum_gdd, soil_ph, n, p, k, oc, rain_anom]]
pred = model.predict(input_data)[0]

st.success(f"ಇಳುವರಿ: **{pred:.0f} ಕೆ.ಜಿ/ಹೆಕ್ಟೇರ್**")
st.success(f"Yield: **{pred:.0f} kg/ha**")

if pred < 4500:
    st.warning("ಗಮನ: ಕಡಿಮೆ ಇಳುವರಿ ಅಪಾಯ! ಬೀಜದ ಸಾಂದ್ರತೆ ಕಡಿಮೆ ಮಾಡಿ।")
else:
    st.info("ಉತ್ತಮ ಬೆಳೆಯ ಸಾಧ್ಯತೆ!")
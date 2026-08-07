# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 20:34:49 2026

@author: VICTUS
"""

import streamlit as st
import joblib
import numpy as np
from PIL import Image
import tempfile

from decision_engine import get_action
from gps_logger import initialize_log, log_data

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")

initialize_log()

st.set_page_config(
    page_title="AgriEdge",
    page_icon="🌾",
    layout="centered"
)
st.title("🌾 AgriEdge")
st.subheader("Indigenous Edge AI Drone Platform for Precision Agriculture for NorthEast India")
st.write("AI-based crop disease detection, autonomous decision support and GPS mission logging.")


uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", width=400)

    if st.button("Predict"):

        img = image.resize((64,64))

        img_array = np.array(img).flatten().reshape(1,-1)

        prediction = model.predict(img_array)

        predicted_class = encoder.inverse_transform(prediction)[0]

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(img_array)

            confidence = float(np.max(probability)*100)

        else:

            confidence = 0.0

        decision = get_action(
            predicted_class,
            confidence
        )

        latitude = 23.7271
        longitude = 92.7176

        log_data(
            "WP1",
            latitude,
            longitude,
            predicted_class,
            round(confidence,2),
            decision["Status"],
            decision["Action"],
            decision["Priority"]
        )

        st.success("Prediction Completed")

        st.write("### Prediction")

        crop = predicted_class.split("___")[0].replace("_", " ")
        disease = predicted_class.split("___")[1].replace("_", " ")

        st.write("**Crop:**", crop)
        st.write("**Disease:**", disease)

        if confidence >= 10:
          st.success(f"Confidence: {confidence:.2f}%")
        else:
          st.warning(f"Confidence: {confidence:.2f}%")

        st.write("### Drone Decision")

        if decision["Status"] == "Healthy":
          st.success("🟢 Healthy Crop")

        elif decision["Status"] == "Disease Detected":
          st.error("🔴 Disease Detected")

        else:
          st.warning("🟡 Uncertain Prediction")

        st.write("**Recommended Action:**", decision["Action"])

        st.write("**Priority:**", decision["Priority"])

        st.write("### GPS")

        st.write("Latitude :", latitude)

        st.write("Longitude :", longitude)

        st.success("Mission Logged Successfully")

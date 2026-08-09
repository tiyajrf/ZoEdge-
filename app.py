# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 20:34:49 2026

@author: VICTUS
"""

import streamlit as st
import joblib
import numpy as np
from PIL import Image

from decision_engine import get_action
from gps_logger import initialize_log, log_data


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ZoEdge",
    page_icon="🌾",
    layout="centered"
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    encoder = joblib.load("encoder.pkl")
    return model, encoder


model, encoder = load_model()


# =========================================================
# INITIALIZE GPS LOG
# =========================================================

initialize_log()


# =========================================================
# HEADER
# =========================================================

st.title("🌾 ZoEdge")

st.subheader(
    "Indigenous Edge AI Drone Platform for Precision Agriculture "
    "for Northeast India"
)

st.write(
    "AI-based crop disease detection, autonomous decision support "
    "and GPS mission logging."
)


# =========================================================
# IMAGE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    # -----------------------------------------------------
    # LOAD IMAGE
    # -----------------------------------------------------

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Crop Image",
        width=400
    )


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    if st.button("🔍 Predict Disease", use_container_width=True):

        try:

            # =================================================
            # IMAGE PREPROCESSING
            # =================================================

            img = image.resize((64, 64))

            img_array = np.array(img, dtype=np.float32)

            # Flatten image exactly as used by the current model
            img_array = img_array.flatten().reshape(1, -1)


            # =================================================
            # MODEL PREDICTION
            # =================================================

            prediction = model.predict(img_array)

            predicted_class = encoder.inverse_transform(
                prediction
            )[0]

            predicted_class = str(predicted_class)


            # =================================================
            # CONFIDENCE
            # =================================================

            if hasattr(model, "predict_proba"):

                probability = model.predict_proba(img_array)

                confidence = float(
                    np.max(probability) * 100
                )

            else:

                confidence = 0.0


            # =================================================
            # SAFELY EXTRACT CROP + DISEASE
            # =================================================

            parts = predicted_class.split("___", 1)

            crop = parts[0].replace("_", " ").strip()

            if len(parts) > 1:
                disease = parts[1].replace("_", " ").strip()
            else:
                disease = "Unknown"


            # =================================================
            # DECISION ENGINE
            # =================================================

            decision = get_action(
                predicted_class,
                confidence
            )


            # =================================================
            # GPS
            # =================================================

            # Demonstration coordinates
            latitude = 23.7271
            longitude = 92.7176


            # =================================================
            # LOG MISSION DATA
            # =================================================

            log_data(
                "WP1",
                latitude,
                longitude,
                predicted_class,
                round(confidence, 2),
                decision["Status"],
                decision["Action"],
                decision["Priority"]
            )


            # =================================================
            # RESULTS
            # =================================================

            st.success("✅ Prediction Completed")


            # -------------------------------------------------
            # PREDICTION
            # -------------------------------------------------

            st.write("### 🌿 Prediction")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Crop**")
                st.info(crop)

            with col2:
                st.write("**Disease**")
                st.warning(disease)


            # -------------------------------------------------
            # CONFIDENCE
            # -------------------------------------------------

            st.write("### 🎯 Model Confidence")

            st.progress(
                min(int(confidence), 100)
            )

            st.write(
                f"**Confidence: {confidence:.2f}%**"
            )


            # -------------------------------------------------
            # DRONE DECISION
            # -------------------------------------------------

            st.write("### 🚁 Drone Decision")


            status = decision["Status"]

            if status == "Healthy":

                st.success(
                    "🟢 Healthy Crop"
                )

            elif status == "Disease Detected":

                st.error(
                    "🔴 Disease Detected"
                )

            else:

                st.warning(
                    "🟡 Uncertain / Possible Disease"
                )


            st.write(
                "**Status:**",
                decision["Status"]
            )

            st.write(
                "**Recommended Action:**",
                decision["Action"]
            )

            st.write(
                "**Priority:**",
                decision["Priority"]
            )


            # -------------------------------------------------
            # PRECISION AGRICULTURE
            # -------------------------------------------------

            st.write("### 🎯 Precision Agriculture")

            if status == "Disease Detected":

                st.success(
                    "🎯 Targeted treatment recommended for "
                    "the detected disease zone."
                )

                st.write(
                    "The detected location can be used as a "
                    "precision-treatment waypoint."
                )

                st.write(
                    "**Treatment Mode:** Precision Spray"
                )

            elif status == "Healthy":

                st.info(
                    "No treatment required. Continue monitoring."
                )

            else:

                st.warning(
                    "Insufficient confidence for treatment. "
                    "Capture additional images before spraying."
                )


            # -------------------------------------------------
            # GPS
            # -------------------------------------------------

            st.write("### 📍 GPS Mission Data")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Latitude",
                    f"{latitude:.4f}"
                )

            with col2:
                st.metric(
                    "Longitude",
                    f"{longitude:.4f}"
                )


            st.success(
                "📡 Mission Logged Successfully"
            )


        except Exception as e:

            st.error(
                "Prediction failed."
            )

            st.exception(e)

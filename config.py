# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:49:55 2026

@author: VICTUS
"""

# config.py

PROJECT_NAME = "AgriEdge"

MODEL_NAME = "MobileNetV3"

CONFIDENCE_THRESHOLD = 0.70

MISSION_NAME = "Precision Agriculture"

CLASSES = [
    "Healthy",
    "Disease",
    "Weed",
    "Nutrient_Stress"
]

ACTIONS = {
    "Healthy": "Continue Mission",
    "Disease": "Precision Spray",
    "Weed": "Selective Herbicide",
    "Nutrient_Stress": "Farmer Notification"
}
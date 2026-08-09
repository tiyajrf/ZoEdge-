# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:46:26 2026

@author: VICTUS
"""

def get_action(predicted_class, confidence):

    predicted_class = predicted_class.lower()

    # Healthy crop
    if "healthy" in predicted_class:
        return {
            "Status": "Healthy",
            "Action": "Continue Monitoring",
            "Treatment": "No Treatment Required",
            "Priority": "Low"
        }

    # High-confidence disease detection
    elif confidence >= 85:
        return {
            "Status": "Disease Detected",
            "Action": "Precision Spray Required",
            "Treatment": "Targeted Treatment Recommended",
            "Priority": "High"
        }

    # Moderate confidence
    elif confidence >= 60:
        return {
            "Status": "Possible Disease",
            "Action": "Capture More Images",
            "Treatment": "Hold Spray Decision",
            "Priority": "Medium"
        }

    # Low confidence
    else:
        return {
            "Status": "Uncertain",
            "Action": "Capture More Images",
            "Treatment": "No Spray",
            "Priority": "Low"
        }


if __name__ == "__main__":

    result = get_action(
        "Tomato___Late_blight",
        91
    )

    print(result)

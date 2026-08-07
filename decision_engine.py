# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:46:26 2026

@author: VICTUS
"""

def get_action(predicted_class, confidence):

    predicted_class = predicted_class.lower()

    if "healthy" in predicted_class:
        return {
            "Status": "Healthy",
            "Action": "Continue Mission",
            "Priority": "Low"
        }

    elif confidence >= 70:
        return {
            "Status": "Disease Detected",
            "Action": "Precision Spray Required",
            "Priority": "High"
        }

    else:
        return {
            "Status": "Possible Disease",
            "Action": "Capture More Images",
            "Priority": "Medium"
        }


if __name__ == "__main__":

    result = get_action(
        "Tomato___Late_blight",
        85
    )

    print(result)
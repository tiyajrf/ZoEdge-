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
            "Priority": "Low"
        }

    # High enough confidence for precision-treatment recommendation
    elif confidence >= 65:
        return {
            "Status": "Disease Detected",
            "Action": "Precision Spray Required",
            "Priority": "High"
        }

    # Moderate confidence
    elif confidence >= 50:
        return {
            "Status": "Possible Disease",
            "Action": "Capture More Images",
            "Priority": "Medium"
        }

    # Low confidence
    else:
        return {
            "Status": "Uncertain",
            "Action": "Capture More Images",
            "Priority": "Low"
        }


# Test
if __name__ == "__main__":

    result = get_action(
        "Pepper__bell___Bacterial_spot",
        67
    )

    print(result)

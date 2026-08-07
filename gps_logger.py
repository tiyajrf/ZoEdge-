# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:51:48 2026

@author: VICTUS
"""

import csv
import os
from datetime import datetime

CSV_FILE = "gps_log.csv"

def initialize_log():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp",
                "Waypoint",
                "Latitude",
                "Longitude",
                "Disease",
                "Confidence",
                "Status",
                "Action",
                "Priority"
            ])

def log_data(waypoint, latitude, longitude, disease, confidence, status, action, priority):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            waypoint,
            latitude,
            longitude,
            disease,
            confidence,
            status,
            action,
            priority
        ])
"""
ambulance.py  –  Smart Ambulance System
Developer   : Chidera Akujieze
Component   : Ambulance System (MQTT Publisher)
Repository  : smart-ambulance-
Description : Connects to an MQTT broker and publishes patient health data
              (condition, heart rate, oxygen level, ETA, paramedic, treatment)
              to the topic  ambulance/patient  every 10 seconds.

How to run it :
  1. Install dependencies:   pip install paho-mqtt
  2. Run this file:           python ambulance.py
"""

import paho.mqtt.client as mqtt
import json
import time
import random

# ── MQTT Configuration ──────────────────────────────────────────────────────
BROKER = "test.mosquitto.org"
PORT   = 1883
TOPIC  = "ambulance/patient"

# ── Ambulance & Paramedic Details ───────────────────────────────────────────
AMBULANCE_ID = "A1"
PARAMEDIC    = "Tobias Gonzalez"
TREATMENTS   = [
    "Leg stabilised",
    "Oxygen administered",
    "Pain relief given",
    "Bandage applied",
    "Neck brace fitted",
]

# ── Patient Data Simulation ─────────────────────────────────────────────────
def get_patient_data():
    """
    Simulates patient sensor readings.
    Returns a dictionary with condition, heart rate, oxygen level and status.
    In a real system this data would come from medical hardware or patient_monitor.py.
    """
    conditions = ["Broken Leg", "Chest Pain", "Broken Arm", "Head Injury"]
    return {
        "patient_id": 2,
        "condition":  random.choice(conditions),
        "heart_rate": random.randint(70, 110),   # bpm  – realistic range
        "oxygen":     random.randint(90, 99),    # %SpO2 – realistic range
        "status":     random.choice(["Stable", "Critical"]),
    }

# ── Build and Publish Message ───────────────────────────────────────────────
def send_data(client):
    """
    Builds the full message dictionary, serialises it to JSON and publishes
    it to the MQTT broker on the configured topic.
    """
    patient   = get_patient_data()
    eta       = random.randint(3, 10)
    treatment = random.choice(TREATMENTS)

    message = {
        "ambulance":  AMBULANCE_ID,
        "patient_id": patient["patient_id"],
        "condition":  patient["condition"],
        "heart_rate": patient["heart_rate"],
        "oxygen":     patient["oxygen"],
        "status":     patient["status"],
        "eta":        f"{eta} minutes",     # string with units as expected by hospital.py
        "paramedic":  PARAMEDIC,
        "treatment":  treatment,
    }

    payload = json.dumps(message)          # convert dict → JSON string for MQTT
    client.publish(TOPIC, payload)

    # Print confirmation to terminal (acts as simple dashboard / UI)
    timestamp = time.strftime("%H:%M:%S")
    print(f"\n[Ambulance {AMBULANCE_ID}] Message sent at {timestamp}")
    print("-" * 50)
    for key, value in message.items():
        print(f"  {key:<12}: {value}")
    print("-" * 50)

# ── MQTT Callbacks ──────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    """Called automatically when the client connects to the broker."""
    if rc == 0:
        print(f"✓ Connected to MQTT Broker  [{BROKER}:{PORT}]  successfully.")
    else:
        print(f"✗ Connection failed — return code {rc}")

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    client = mqtt.Client()
    client.on_connect = on_connect      # attach callback

    print(f"Ambulance {AMBULANCE_ID} starting up...")
    client.connect(BROKER, PORT, 60)    # connect to broker (keepalive = 60 s)
    client.loop_start()                 # start background network thread

    print(f"Sending patient data every 10 seconds to topic: {TOPIC}\n")
    try:
        while True:
            send_data(client)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nAmbulance system stopped by user.")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Settings
BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

# Ambulance details
AMBULANCE_ID = "A1"
PARAMEDIC = "Tobias Gonzalez"
TREATMENTS = ["Leg stabilised", "Oxygen administered", "Pain relief given", "Bandage applied"]

def get_patient_data():
    conditions = ["Broken Leg", "Chest Pain", "Broken Arm", "Head Injury"]
    return {
        "patient_id": 2,
        "condition": random.choice(conditions),
        "heart_rate": random.randint(70, 110),
        "oxygen": random.randint(90, 99),
        "status": random.choice(["Stable", "Critical"])
    }

def send_data(client):
    patient = get_patient_data()
    eta = random.randint(3, 10)
    treatment = random.choice(TREATMENTS)

    message = {
        "ambulance": AMBULANCE_ID,
        "patient_id": patient["patient_id"],
        "condition": patient["condition"],
        "heart_rate": patient["heart_rate"],
        "oxygen": patient["oxygen"],
        "status": patient["status"],
        "eta": f"{eta} minutes",
        "paramedic": PARAMEDIC,
        "treatment": treatment
    }

    payload = json.dumps(message)
    client.publish(TOPIC, payload)
    print(f"\n[Ambulance {AMBULANCE_ID}] Data sent:")
    print(payload)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully.")
    else:
        print(f"Connection failed with code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

print(f"Ambulance {AMBULANCE_ID} running...")
while True:
    send_data(client)
    time.sleep(10)

import paho.mqtt.client as mqtt
import json
import time
import database

BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

VALID_USERS = {
    "admin": "hospital123",
    "Tobias": "123456",
    "doctor": "pass2026",
}


def login():
    print("=" * 40)
    print("       HOSPITAL SYSTEM LOGIN")
    print("=" * 40)

    attempts = 3

    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if VALID_USERS.get(username) == password:
            print(f"\nLogin successful. Welcome, {username}!\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect credentials. {attempts} attempt(s) remaining.\n")

    print("Access denied. Exiting.")
    return False


def display_patient_update(data):
    print("\n" + "=" * 50)
    print("PATIENT UPDATE RECEIVED")
    print("=" * 50)
    print(f"Ambulance: {data.get('ambulance', 'N/A')}")
    print(f"Patient ID: {data.get('patient_id', 'N/A')}")
    print(f"Condition: {data.get('condition', 'N/A')}")
    print(f"Heart Rate: {data.get('heart_rate', 'N/A')} bpm")
    print(f"Oxygen Level: {data.get('oxygen', 'N/A')} %")
    print(f"Status: {data.get('status', 'N/A')}")
    print(f"ETA: {data.get('eta', 'N/A')}")
    print(f"Paramedic: {data.get('paramedic', 'N/A')}")
    print(f"Treatment: {data.get('treatment', 'N/A')}")
    print("=" * 50)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker [{BROKER}:{PORT}]")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed — return code {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        display_patient_update(data)
        database.save_record(data)
    except json.JSONDecodeError:
        print("Received malformed message")


def main():
    if not login():
        return

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()

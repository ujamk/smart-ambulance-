import paho.mqtt.client as mqtt
import json

BROKER = "test.mosquitto.org"
TOPIC = "ambulance/patient"

def on_connect(client, userdata, flags, rc):
    print("Test client connected." if rc == 0 else f"Failed: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("[TEST] Message received:")
    print(data)
    client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()

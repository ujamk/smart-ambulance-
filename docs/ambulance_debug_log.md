# ambulance_debug_log.md
## Smart Ambulance System, Ambulance Component Debugging Journal

**Developer:** Chidera Akujieze  
**File:** `ambulance.py`  
**Project:** Smart Ambulance System  
**Dates:** Week 3–4 (09 March – 22 March 2026)

---

## Overview

This document I created records the full iterative debugging process for my `ambulance.py`. It includes each code version, a list of all identified mistakes, team conversations via Microsoft Teams and GitHub Issues, and the updated code produced after applying feedback gieven by the group members. The file serves as evidence of the Agile development process, collaborative problem-solving, and individual learning progression.

---

## GitHub Commit History

| Commit | Message | Date |
|--------|---------|------|
| `a1f3c9` | Initial ambulance system with multiple errors | 09 Mar 2026 |
| `b2d7e1` | Fixed syntax issues after team discussion | 13 Mar 2026 |
| `c4e8a2` | Resolved MQTT and JSON formatting problems | 17 Mar 2026 |
| `d5f9b3` | Improved data structure and added missing fields | 19 Mar 2026 |
| `e6g0c4` | Final working ambulance system — all tests pass | 22 Mar 2026 |

---

## GitHub Issues

| Issue # | Title | Status |
|---------|-------|--------|
| #1 | Fix MQTT connection error — broker refusing connection | Closed |
| #2 | Debug JSON formatting — hospital receiving garbled data | Closed |
| #3 | Hospital not receiving data — message not being published | Closed |
| #4 | Loop flooding broker — missing time delay | Closed |
| #5 | Patient data fields incomplete — missing ETA and treatment | Closed |

---

---

# ITERATION 1, Initial Broken Code

**Commit:** `a1f3c9`, "Initial ambulance system with multiple errors"  
**Date:** 09 March 2026

---

## Code (Version 1, BROKEN)

```python
import paho.mqtt.client as mqtt
import json
import time

# MQTT setttings
BROKER = "localhosr"   # ERROR 1: typo in broker address
PORT = 188             # ERROR 2: wrong port number (should be 1883)
TOPIC_SUBSCRIBE = "ambulance/patientdata"   # ERROR 3: wrong topic name
TOPIC_PUBLISH = "hospital"   # ERROR 4: incomplete topic name

# Patient data — ERROR 5: missing required fields (no ETA, paramedic, treatment)
patient_data = {
    "patient_id": 1,
    "condition": "Broken Leg",
    "heart_rate": 89,
    "oxygen": 97,
    "status": "Stable"
}

# ERROR 6: json.dump() used instead of json.dumps()
message = json.dump(patient_data)

def on_connect(client, userdata, flags, rc)
    # ERROR 7: missing colon at end of function definition
    print("Connected to broker")

def on_message(client, userdata, msg)
    # ERROR 8: missing colon at end of function definition
    print("Message received" + msg.payload)
    # ERROR 9: cannot concatenate str and bytes directly

client = mqtt.Client
# ERROR 10: Client class not instantiated — missing parentheses ()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

# ERROR 11: publishing raw dictionary instead of JSON string
client.publish(TOPIC_PUBLISH, patient_data)

# ERROR 12: no loop or sleep — would send once and stop immediately
```

---

## List of All Mistakes (Iteration 1)

- **Error 1:** Typo in broker address — `"localhosr"` should be `"localhost"`
- **Error 2:** Wrong MQTT port — `188` should be `1883`
- **Error 3:** Wrong subscribe topic — `"ambulance/patientdata"` should be `"ambulance/patient_data"`
- **Error 4:** Incomplete publish topic — `"hospital"` should be `"hospital/patient_data"`
- **Error 5:** Missing required fields — no ETA, paramedic name, treatment, or ambulance ID in the data
- **Error 6:** `json.dump()` used instead of `json.dumps()` — `json.dump()` writes to a file, not a string
- **Error 7:** Missing colon at end of `on_connect` function definition — SyntaxError
- **Error 8:** Missing colon at end of `on_message` function definition — SyntaxError
- **Error 9:** String concatenation with bytes — `msg.payload` is bytes, must decode first
- **Error 10:** `mqtt.Client` used without `()` — this assigns the class itself, not an instance
- **Error 11:** Raw Python dictionary passed to `client.publish()` — must publish a string
- **Error 12:** No `time.sleep()` in loop — system would publish once and exit

---

## Team Conversation (Microsoft Teams, 09 March 2026)

> **Me** Hey everyone, I've written the first version of ambulance.py but it's throwing multiple errors and I can't run it at all. I'm getting SyntaxErrors immediately. I'll paste the code below — can anyone have a look?

> **Mohamad Radwan (Patient Monitor developer):**
> I can see two immediate SyntaxErrors, your `on_connect` and `on_message` function definitions are missing the colon `:` at the end. In Python, every `def` line must end with a colon. Also, on line where you do `client = mqtt.Client`, you're assigning the *class* to the variable, not creating an *instance* of it. You need `mqtt.Client()` with parentheses. Without the `()`, you haven't actually created a client object, so calling `.connect()` on it will fail.

> **Kosi Ujam (Hospital System developer):**
> Also, I noticed you're using `json.dump()`, that function is for writing JSON *to a file*. What you want is `json.dumps()` with an `s` at the end, which converts a dictionary to a *string*. Then you need to pass *that string* to `client.publish()`. Right now you're trying to publish a raw Python dictionary, and MQTT only accepts strings or bytes. I'd also double-check your broker address, `"localhosr"` looks like a typo.

> **Mario Brunovsky (Database developer):**
> Try adding `print(message)` right before the publish call so you can see what you're actually sending. That way you'll know immediately if the JSON looks right. Also your port number is 188, it should be 1883. And in the `on_message` callback, `msg.payload` gives you bytes, not a string, you need to do `msg.payload.decode('utf-8')` to convert it.

> **Me** Thanks all, really helpful. I'll fix these and push a new version.

---

---

# ITERATION 2, Partial Fix (Still Has Errors)

**Commit:** `b2d7e1` — "Fixed syntax issues after team discussion"  
**Date:** 13 March 2026

---

## Code (Version 2, PARTIALLY FIXED)

```python
import paho.mqtt.client as mqtt
import json
import time

# MQTT settings
BROKER = "localhost"    # Fixed Error 1
PORT = 1883             # Fixed Error 2
TOPIC_SUBSCRIBE = "ambulance/patient_data"   # Fixed Error 3
TOPIC_PUBLISH = "hospital/patient_data"      # Fixed Error 4

# ERROR A: still missing ambulance ID, ETA, paramedic, treatment
patient_data = {
    "patient_id": 1,
    "condition": "Broken Leg",
    "heart_rate": 89,
    "oxygen": 97,
    "status": "Stable"
}

# Fixed Error 6 — but ERROR B: message built before client connects or receives data
message = json.dumps(patient_data)

def on_connect(client, userdata, flags, rc):   # Fixed Errors 7 & 8
    print("Connected to broker")
    # ERROR C: not subscribing inside on_connect — subscription must happen after connection

def on_message(client, userdata, msg):   # Fixed Error 8
    data = msg.payload.decode('utf-8')   # Fixed Error 9
    print("Received: " + data)
    # ERROR D: received data from patient monitor but not enriching it with ambulance fields

client = mqtt.Client()   # Fixed Error 10
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

# ERROR E: client.loop_start() not called — background network loop not running
# This means the client will connect but never process incoming messages

# Fixed Error 11
client.publish(TOPIC_PUBLISH, message)

# ERROR F: no continuous loop — only publishes once and exits
# ERROR G: publishes before receiving data from patient monitor
time.sleep(1)
```

---

## List of Mistakes (Iteration 2)

- **Error A:** Patient data still incomplete — ambulance ID, ETA, paramedic, and treatment fields are missing
- **Error B:** `json.dumps()` called immediately on hardcoded data rather than on dynamically received data from patient monitor
- **Error C:** MQTT subscription (`client.subscribe()`) not called inside `on_connect` — the topic is never actually subscribed to
- **Error D:** `on_message` receives data from patient monitor but does not add ambulance-specific fields before forwarding
- **Error E:** `client.loop_start()` not called — the background network thread is not running, so the client cannot receive messages
- **Error F:** No while loop with `time.sleep(10)` — system publishes once and exits rather than looping
- **Error G:** Publish occurs before any data has been received from the patient monitor

---

## GitHub Issue Posted (#3): "Hospital not receiving data"

> **[Your Name] opened issue #3:**
> ambulance.py connects successfully to the broker now, but hospital.py is not receiving any messages. I confirmed the broker is running. I suspect the publish isn't working correctly but I'm not sure why. Can anyone check?

> **Member A replied:**
> Check whether you've called `client.loop_start()` after `client.connect()`. Without it, the Paho client's background thread isn't running and it can't process the network I/O — meaning messages are queued but never actually sent. This is one of the most common Paho mistakes.

> **Member B replied:**
> Also, you need to subscribe to the patient monitor topic *inside* the `on_connect` callback, not before. The correct pattern is: define `on_connect`, then inside it call `client.subscribe(TOPIC_SUBSCRIBE)`. That way the subscription is registered as soon as the connection is confirmed. Moving it outside that callback means you might try to subscribe before the connection is established, which silently fails.

> **Member C replied:**
> Once you've sorted the loop and subscription, make sure your `on_message` function isn't just printing the data — it should be storing the received patient data somewhere (e.g., a global variable) so the publish loop can pick it up and send it to the hospital. Right now you're receiving the data but not doing anything with it.

---

---

# ITERATION 3, Almost Correct (Minor Issues)

**Commit:** `c4e8a2` — "Resolved MQTT and JSON formatting problems"  
**Date:** 17 March 2026

---

## Code (Version 3 — NEARLY CORRECT)

```python
import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC_SUBSCRIBE = "ambulance/patient_data"
TOPIC_PUBLISH = "hospital/patient_data"
AMBULANCE_ID = "A1"

# Global variable to store received patient data
received_data = {}

def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code: " + str(rc))
    client.subscribe(TOPIC_SUBSCRIBE)   # Fixed Error C
    print("Subscribed to: " + TOPIC_SUBSCRIBE)

def on_message(client, userdata, msg):
    global received_data
    data = msg.payload.decode('utf-8')
    received_data = json.loads(data)   # Fixed Error D — storing received data
    print("Received patient data from monitor")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()   # Fixed Error E

# ERROR H: ETA calculated incorrectly — using string instead of int then adding "minutes"
eta = "7 minutes"   # should be generated as int and formatted separately

# ERROR I: while loop missing — only sends once
time.sleep(2)  # wait for first message

ambulance_message = {
    "ambulance_id": AMBULANCE_ID,
    "patient_id": received_data.get("patient_id"),
    "condition": received_data.get("condition"),
    "heart_rate": received_data.get("heart_rate"),
    "oxygen": received_data.get("oxygen"),
    "status": received_data.get("status"),
    "eta": eta,
    "paramedic": "Tobias Gonzalez",
    "treatment": "Leg stabilised"   # ERROR J: treatment hardcoded, not dynamically selected
}

message_str = json.dumps(ambulance_message)
print("Sending:", message_str)
client.publish(TOPIC_PUBLISH, message_str)

# ERROR I continued: no while loop — publishes exactly once and stops
time.sleep(10)
client.loop_stop()
```

---

## List of Mistakes (Iteration 3)

- **Error H:** ETA hardcoded as string `"7 minutes"` — should be dynamically generated as a countdown integer, formatted as `f"{eta} minutes"`
- **Error I:** No `while True` loop — the system publishes one message and exits rather than sending every 10 seconds
- **Error J:** Treatment is hardcoded as `"Leg stabilised"` rather than being selected based on the patient's condition

---

## Team Conversation (Teams, 17 March 2026)

> **Me** Much better now, the hospital is receiving messages. But it only receives one message and then stops. I think I'm missing the loop. Also should the ETA be counting down?

> **Mohamad Radwan**
> Yes, you need a `while True:` loop after your initial setup, with `time.sleep(10)` at the bottom of each iteration. Inside the loop, rebuild the ambulance message each time so you pick up fresh data from the patient monitor. The ETA should also decrement each loop, start at, say, 8 and subtract 1 each iteration until it reaches 0 (arrived). You can use `random.randint(5, 10)` for an initial ETA to make it more realistic.

> **Kosi Ujam**
> For the treatment field, consider creating a simple dictionary that maps conditions to standard treatments. For example: `treatments = {"Broken Leg": "Leg stabilised", "Chest Pain": "Oxygen administered", "Broken Arm": "Arm immobilised"}`. Then look up `treatments.get(condition, "Monitoring vital signs")` dynamically.

> **Mario Brunovsky**
> Good progress. Just make sure you also handle the case where `received_data` is still empty when the loop first runs, add an `if received_data:` check before publishing, otherwise you'll send an empty message on the very first iteration if the patient monitor hasn't responded yet.

---

---

# ITERATION 4, Fully Working Code

**Commit:** `e6g0c4`, "Final working ambulance system — all tests pass"  
**Date:** 22 March 2026

---

## Code (Version 4, COMPLETE AND WORKING)

```python
"""
ambulance.py, Smart Ambulance System
Developer: Chidera AKujieze
Role: Ambulance System Component
Description:
    This script represents the ambulance device in the Smart Ambulance System.
    It subscribes to patient data published by the patient monitor,
    enriches the data with ambulance-specific information (ETA, paramedic, treatment),
    and publishes the combined message to the hospital system every 10 seconds via MQTT.
"""

import paho.mqtt.client as mqtt
import json
import time
import random

# ─── MQTT Configuration ──────────────────────────────────────────────────────
BROKER = "localhost"
PORT = 1883
TOPIC_SUBSCRIBE = "ambulance/patient_data"   # Topic published by patient_monitor.py
TOPIC_PUBLISH = "hospital/patient_data"      # Topic consumed by hospital.py
AMBULANCE_ID = "A1"

# ─── Treatment Lookup Table ───────────────────────────────────────────────────
TREATMENTS = {
    "Broken Leg": "Leg stabilised with splint",
    "Broken Arm": "Arm immobilised and sling applied",
    "Chest Pain": "Oxygen administered, ECG monitored",
    "Cardiac Arrest": "CPR performed, defibrillator used",
    "Stroke": "Airway secured, IV line established",
    "Trauma": "Wound dressed, pressure applied",
}
DEFAULT_TREATMENT = "Monitoring vital signs"

# ─── Paramedic on duty ────────────────────────────────────────────────────────
PARAMEDIC = "Tobias Gonzalez"

# ─── Global state ─────────────────────────────────────────────────────────────
received_data = {}       # Stores the latest patient data from the patient monitor
eta_minutes = random.randint(6, 10)   # Initial ETA in minutes


# ─── MQTT Callbacks ───────────────────────────────────────────────────────────

def on_connect(client, userdata, flags, rc):
    """Called when the client connects to the MQTT broker."""
    if rc == 0:
        print("=" * 50)
        print("  AMBULANCE SYSTEM CONNECTED TO BROKER")
        print("=" * 50)
        client.subscribe(TOPIC_SUBSCRIBE)
        print(f"  Subscribed to topic: {TOPIC_SUBSCRIBE}")
        print(f"  Ambulance ID: {AMBULANCE_ID}")
        print(f"  Paramedic: {PARAMEDIC}")
        print(f"  Initial ETA: {eta_minutes} minutes")
        print("=" * 50)
    else:
        print(f"Connection failed with result code {rc}")


def on_message(client, userdata, msg):
    """Called when a message is received from the patient monitor."""
    global received_data
    try:
        payload = msg.payload.decode("utf-8")
        received_data = json.loads(payload)
        print(f"\n[AMBULANCE] Patient data received from monitor.")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"[AMBULANCE] Error decoding incoming message: {e}")


# ─── Build and publish ambulance message ─────────────────────────────────────

def build_and_publish(client):
    """Enrich patient monitor data with ambulance fields and publish to hospital."""
    global eta_minutes

    if not received_data:
        print("[AMBULANCE] Waiting for patient data from monitor...")
        return

    condition = received_data.get("condition", "Unknown")
    treatment = TREATMENTS.get(condition, DEFAULT_TREATMENT)

    ambulance_message = {
        "ambulance_id": AMBULANCE_ID,
        "patient_id": received_data.get("patient_id", 1),
        "condition": condition,
        "heart_rate": received_data.get("heart_rate", 0),
        "oxygen": received_data.get("oxygen", 0),
        "status": received_data.get("status", "Unknown"),
        "eta": f"{eta_minutes} minutes" if eta_minutes > 0 else "Arrived",
        "paramedic": PARAMEDIC,
        "treatment": treatment,
    }

    message_str = json.dumps(ambulance_message)

    # Display the message being sent
    print("\n" + "─" * 50)
    print("  AMBULANCE MESSAGE SENT TO HOSPITAL")
    print("─" * 50)
    for key, value in ambulance_message.items():
        print(f"  {key.capitalize():<15}: {value}")
    print("─" * 50)

    # Publish to hospital
    result = client.publish(TOPIC_PUBLISH, message_str)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"  [OK] Message published to {TOPIC_PUBLISH}")
    else:
        print(f"  [ERROR] Publish failed with code {result.rc}")

    # Decrement ETA (minimum 0)
    if eta_minutes > 0:
        eta_minutes -= 1


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("[AMBULANCE] Connecting to MQTT broker...")
    client.connect(BROKER, PORT)
    client.loop_start()

    # Allow time for the first patient monitor message to arrive
    time.sleep(2)

    try:
        while True:
            build_and_publish(client)
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[AMBULANCE] System stopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[AMBULANCE] Disconnected from broker.")


if __name__ == "__main__":
    main()
```

---

## Summary of All Changes (Iteration 4 vs Iteration 1)

| Issue | Status |
|-------|--------|
| Typo in broker address | Fixed |
| Wrong port number | Fixed |
| Wrong MQTT topics | Fixed |
| Missing required data fields | Fixed — all fields present |
| `json.dump()` → `json.dumps()` | Fixed |
| Missing colons in function definitions | Fixed |
| Bytes/string concatenation | Fixed |
| `mqtt.Client` not instantiated | Fixed |
| Raw dict passed to publish | Fixed |
| `client.loop_start()` missing | Fixed |
| No continuous while loop | Fixed — runs every 10 seconds |
| No MQTT subscription in `on_connect` | Fixed |
| ETA hardcoded | Fixed — dynamic countdown |
| Treatment hardcoded | Fixed — lookup table by condition |
| No error handling | Fixed — try/except on message decode |
| Publishes before data received | Fixed — `if not received_data` guard |

---

*End of Debug Log — ambulance.py*


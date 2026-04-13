# ambulance.py Debug Log
**Developer:** Chidera Akujieze
**File:** ambulance.py
**What it does:** MQTT publisher — sends patient data from the ambulance to the hospital every 10 seconds
**Period:** Week 2 to Week 5

---

## Summary of Iterations

| Iteration | Errors Found | Status |
|-----------|-------------|--------|
| 1 | 9 errors | broken — does not run at all |
| 2 | 4 errors | connects but sends wrong data |
| 3 | 2 errors | almost working — minor field issues |
| 4 | 0 errors | fully working |

---

## Iteration 1 — First Attempt (Very Broken)

**Week:** Week 2 (approx. 02/03/2026)

So this was my very first attempt at ambulance.py. I just tried to get something down on paper but it turns out I had about 9 errors in a file that was only like 20 lines long. Python couldn't even open it, it just crashed straight away before running a single line.

```python
import paho.mqtt.client as mqtt
import json

BROKER = "localhost
PORT = 1883
TOPIC = ambulance/patient

def send_data()
    data = {
        patient_id: 2,
        condition: "Broken Leg",
        heart_rate: "92",
        oxygen: 95
        status: "Stable"
        eta: 6,
        paramedic: "Tobias Gonzalez"
        treatment: "Leg stabilised"
    }
    payload = json.dump(data)
    client.publish(TOPIC, data)

send_data()
```

Here is every single thing I got wrong:

- **Error 1 — Unclosed string:** `BROKER = "localhost` is missing the closing quote mark at the end. Python sees this and immediately throws a SyntaxError before it even gets to line 2.
- **Error 2 — TOPIC not a string:** `TOPIC = ambulance/patient` has no quotes around it so Python thinks I am trying to divide a variable called `ambulance` by a variable called `patient`. Neither of those exist so it crashes with a NameError.
- **Error 3 — Missing colon on function:** `def send_data()` needs a colon at the end. Without it Python has no idea the function definition is finished.
- **Error 4 — Dictionary keys not strings:** All the keys like `patient_id`, `condition` etc need to be in quotes. Without quotes Python treats them as variable names which dont exist.
- **Error 5 — heart_rate is a string not a number:** I wrote `"heart_rate": "92"` but heart rate should be an integer `92`. Storing it as a string means the database gets text where it expects a number which breaks everything downstream.
- **Error 6 — Missing comma after oxygen:** `oxygen: 95` has no comma before `status` which is a SyntaxError.
- **Error 7 — Missing commas elsewhere in the dictionary:** Several other key-value pairs also had missing trailing commas throughout.
- **Error 8 — Wrong JSON function:** I used `json.dump(data)` which is for writing JSON to a file. The correct one for producing a JSON string is `json.dumps(data)` with the `s` at the end.
- **Error 9 — Publishing the dictionary instead of the JSON string:** `client.publish(TOPIC, data)` is passing the raw Python dictionary. MQTT needs a string, not a Python object.
- **Error 10 — No MQTT client created or connected:** There is no `client = mqtt.Client()` and no `client.connect()` anywhere. So even if everything else was fixed, calling `client.publish()` would just crash with an AttributeError because `client` doesn't exist. It's basically like trying to make a phone call without ever buying a phone or dialling a number.

After I pushed this to the repo I sent a message to the team on Microsoft Teams explaining it wasnt working and asking for help. Mohamad spotted the missing quote and the TOPIC string issue. Kosi caught the `json.dump` vs `json.dumps` mistake and the fact I was passing `data` instead of `payload`. Mario pointed out that I never actually created or connected the MQTT client in the first place.

---

## Iteration 2 — After First Round of Fixes

**Week:** Week 3 (approx. 09/03/2026)

So after taking on board what the team told me I fixed the syntax errors and added the client object. The code could now actually be parsed by Python which was progress. But it still wasnt working properly. I raised a GitHub Issue (#2) because the broker still wasnt receiving anything.

```python
import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

client = mqtt.Client()

def send_data():
    data = {
        "patient_id": 2,
        "condition": "Broken Leg",
        "heart_rate": "92",        # still wrong — string not int
        "oxygen": 95,
        "status": "Stable",
        "eta": 6,
        "paramedic": "Tobias Gonzalez",
        "treatment": "Leg stabilised"
    }
    payload = json.dumps(data)
    client.publish(TOPIC, data)    # still wrong — should be payload not data

send_data()
```

The remaining mistakes at this point were:

- **Error 1 — heart_rate still a string:** Still had `"heart_rate": "92"` as a string. Should be the integer `92`. The database was going to store text instead of a number and break SQL queries.
- **Error 2 — Still publishing `data` not `payload`:** I created the `payload` variable with the correct JSON string but then on the publish line I passed `data` (the raw dictionary) instead of `payload`. So MQTT was still receiving a Python object, not valid JSON.
- **Error 3 — No client.connect():** I created the client object but forgot to actually connect it to the broker. The `client.connect(BROKER, PORT, 60)` line was completely missing.
- **Error 4 — No loop:** The code called `send_data()` exactly once and then stopped. There was no loop to keep sending every 10 seconds like the plan required.

Kosi replied on the GitHub issue and caught the missing `client.connect()` and the `data` vs `payload` mix-up. Mohamad told me to add a while loop with `time.sleep(10)`. Mario showed me how he had done the same loop in his own file.

---

## Iteration 3 — Almost Working

**Week:** Week 4 (approx. 17/03/2026)

At this point the code was genuinely running and printing "Data sent" every 10 seconds which felt like a big step. But when I checked it against the original plan document I noticed a couple of things were still wrong with the actual data being sent.

The remaining mistakes were:

- **Error 1 — ETA missing units:** `"eta": 6` is just a number. The hospital.py expected a string like `"6 minutes"` so the display was showing a bare number with no context.
- **Error 2 — Ambulance ID missing from the message:** The plan said every message should include the ambulance identifier (like `"ambulance": "A1"`) so the hospital knows which ambulance is sending the data. I had just completely forgotten to include it and Kosi told me his hospital.py was expecting `data['ambulance']` which would crash with a KeyError if the field was absent.
- **Error 3 — No client.loop_start():** Without `client.loop_start()`, the MQTT client's internal background network thread never starts. Mario flagged this — apparently messages can occasionally fail to send without it, especially on slower connections.

I messaged the team on Teams to double-check what format Kosi's hospital.py was expecting for the ambulance ID and ETA fields before I changed anything, because I wanted to make sure my output matched what he needed exactly.

---

## Iteration 4 — Final Working Code ✅

**Week:** Week 5 (approx. 24/03/2026)

This is the final version. Zero errors. Everything the plan asked for is now in the message, the data types are all correct, and the system runs continuously until you press Ctrl+C. I also added some extra things like randomised vitals and conditions to make the simulation feel more realistic, and proper comments throughout the code.

```python
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

---

## All Errors Fixed Across All Iterations

| Error | Fixed in |
|-------|----------|
| Syntax errors (missing quotes, colons, commas) | Iteration 2 |
| MQTT client not created or connected | Iteration 2 |
| json.dump vs json.dumps | Iteration 2 |
| Publishing dictionary instead of JSON string | Iteration 2 |
| heart_rate stored as string not integer | Iteration 3 |
| No loop — only sent once | Iteration 3 |
| ETA missing units | Iteration 4 |
| Ambulance ID missing from message | Iteration 4 |
| client.loop_start() missing | Iteration 4 |

---

## Commit History

```
1. "Initial project structure and README"                     — Week 2
2. "Add first attempt at ambulance.py"                        — Week 2
3. "Fix syntax errors in ambulance.py after team feedback"    — Week 3
4. "Resolve MQTT connection and JSON formatting issues"        — Week 3
5. "Add continuous send loop and fix data types"              — Week 4
6. "Add ambulance ID, fix ETA format, add loop_start"         — Week 4
7. "Final working ambulance system"                           — Week 5
8. "Add MQTT test script and full debug log"                  — Week 6
```

---

*Chidera Akujieze | smart-ambulance- | Coventry University 2026*

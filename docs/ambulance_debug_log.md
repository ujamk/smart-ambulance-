# Ambulance System — Full Debugging Log

**Developer:** Chidera Akujieze
**File:** `src/ambulance.py`  
**Component:** Ambulance System (MQTT Publisher)  
**Period:** Week 2 – Week 6 (February – April 2026)  
**Repository:** smart-ambulance-system

---

## Summary of Iterations

| Iteration | Errors Found | Status |
|-----------|-------------|--------|
| 1 | 9 errors | ❌ Broken — does not run |
| 2 | 4 errors | ❌ Partially broken — connects but sends wrong data |
| 3 | 2 errors | ⚠️ Almost working — minor field issues |
| 4 | 0 errors | ✅ Fully working |

---

## Iteration 1, First Attempt of Creating the Ambulance.py code(Very Broken)

### Date: Week 2 (approx. 02/03/2026)

### Code

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

### List of Mistakes I Made

- **Error 1 : Unclosed string:** `BROKER = "localhost` is missing the closing quotation mark `"`. This causes a `SyntaxError` immediately when Python tries to parse the file.
- **Error 2 : TOPIC not a string:** `TOPIC = ambulance/patient` has no quotation marks. Python treats this as a variable divided by another variable — a `NameError`.
- **Error 3 : Missing colon on function:** `def send_data()` is missing its colon at the end. Python requires `def send_data():`.
- **Error 4 : Dictionary keys not strings:** All dictionary keys (e.g. `patient_id`, `condition`) must be wrapped in quotes: `"patient_id"`, `"condition"`, etc.
- **Error 5 : Wrong data type for heart_rate:** `heart_rate: "92"` stores heart rate as a string. It should be the integer `92` so that the hospital database stores it correctly as a number.
- **Error 6 : Missing comma after `oxygen`:** `oxygen: 95` is missing a comma before `status`. This causes a `SyntaxError`.
- **Error 7 : Missing commas inside dictionary:** Several other key-value pairs are also missing trailing commas.
- **Error 8 : Wrong JSON function:** `json.dump(data)` writes JSON to a file object. The correct function for producing a JSON string is `json.dumps(data)` (with an `s` at the end).
- **Error 9 : Publishing raw dictionary:** `client.publish(TOPIC, data)` passes the Python dictionary instead of the JSON string. MQTT requires a string payload.
- **Error 10 : No MQTT client created or connected:** There is no `client = mqtt.Client()` and no `client.connect()`. Without these, any attempt to call `client.publish()` will raise an `AttributeError`.

### Explanation of why my code for ambulance.py was not working

This code fails before it can even start. Python can't parse the file because of the syntax errors (missing quotes and colon). Even if those were fixed, the MQTT client has never been set up, so there is nothing to publish to. It's like trying to make a phone call without ever buying a phone or entering a number.

---

### Team Message (Microsoft Teams — 02/03/2026)

> **Me:** Goodmorning team, I've written my first version of ambulance.py but it has a lot of errors, it won't even run. Could anyone take a look? I'm getting syntax errors but I think there are other problems too. I've pushed it to the repo under `src/ambulance.py`. Any help would be appreciated.

---

### Member A Response

> **Mohamad Radwan:** Good Afternoon Chidera, I had a look at your code. First thing, line 4: `BROKER = "localhost` is missing a closing quote. That alone will stop everything. Also line 6: `TOPIC = ambulance/patient` needs to be a string in quotes: `TOPIC = "ambulance/patient"`. Python is reading it as variables right now. That is why you got that problem in your coding when trying to run it

---

### Member B Response

> **Kosi Ujam:** You've also used `json.dump` instead of `json.dumps`. The version without the `s` is for writing to a file — you need `json.dumps` which returns a string. MQTT's publish method needs a string. Also, you're passing `data` (the dictionary) to `client.publish` but you should be passing `payload` (the JSON string you created on the line above). Hope this will help you with your issue.

---

### Member C Response

> **Mario Brunovsky:** One more thing, I don't see where you created the MQTT client. You need `client = mqtt.Client()` somewhere before you try to use it. And don't forget `client.connect(BROKER, PORT, 60)` before you call `send_data()`. Try adding a print statement right before `client.publish()` so you can see what's actually being sent. Makes debugging a lot easier. I am sayin these from previous experience where I encounter these same issue.

---

## Iteration 2, After First Round of Fixes thanks to the feedback provided from my group members

### Date: Week 3 (approx. 09/03/2026)

### Code

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
        "heart_rate": "92",        # still wrong - string not int
        "oxygen": 95,
        "status": "Stable",
        "eta": 6,
        "paramedic": "Tobias Gonzalez",
        "treatment": "Leg stabilised"
    }
    payload = json.dumps(data)
    client.publish(TOPIC, data)    # still wrong - should be payload

send_data()
```

### Remaining Mistakes After Applying What My Group Members Told Me Do

- **Error 1 : heart_rate still a string:** `"heart_rate": "92"` should be `"heart_rate": 92`. Storing it as a string means the database will store it as text, not a number, which breaks SQL queries and reporting.
- **Error 2 : Still publishing `data` not `payload`:** The variable `payload` contains the correct JSON string, but `client.publish(TOPIC, data)` is still passing the raw dictionary. This means MQTT receives a Python object representation, not valid JSON.
- **Error 3 : No client.connect():** The MQTT client object was created but never connected to the broker. `client.connect(BROKER, PORT, 60)` is missing.
- **Error 4 : No loop:** The code calls `send_data()` once and exits. There is no loop to send data every 10 seconds as required.

### Explanation of why my code for ambulance.py was not working

Progress has been made, the basic syntax errors are gone and the code can now be parsed by Python. However, the ambulance is still not actually connecting to the MQTT broker, and even if it did, it would send the wrong thing (a Python dictionary instead of a JSON string) just once and then stop.

---

### Team Message (GitHub Issue #2 — 10/03/2026)

> **Title:** Ambulance not sending data to broker  
> **Body:** Thanks to you guys help and replies I could fix the syntax errors from last time but the ambulance system still isn't delivering data. The broker doesn't seem to be receiving anything. I've added the client object but I think I'm still missing something. Please see the latest commit and tell me where I went wrong.

---

### Member B Response (GitHub Issue #2 comment)

> **Kosi Ujam:** You've created the client but haven't connected it. You need `client.connect(BROKER, PORT, 60)` before you call `send_data()`. Also the publish line is still `client.publish(TOPIC, data)`, it needs to be `client.publish(TOPIC, payload)`. You are welcome.

---

### Member A Response

> **Mohamad Radwan:** Also add a while loop with `time.sleep(10)` so it sends every 10 seconds, at the moment it sends once and stops. That's not the behaviour we described in the plan so make sure to apply with the way I described it.

---

### Member C Response

> **Mario Brunovsky:** I tested mine with a similar loop. `import time` at the top and then wrap the call in `while True: send_data(); time.sleep(10)`. That should keep it running, hepefully. Have a try, Chidera.

---

## Iteration 3 : Almost Working

### Date: Week 4 (approx. 17/03/2026)

### Code

```python
import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def send_data():
    data = {
        "patient_id": 2,
        "condition": "Broken Leg",
        "heart_rate": 92,
        "oxygen": 95,
        "status": "Stable",
        "eta": 6,            # should be "6 minutes" (string with units)
        "paramedic": "Tobias Gonzalez",
        "treatment": "Leg stabilised"
        # missing: "ambulance" field
    }
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    print("Data sent:", payload)

while True:
    send_data()
    time.sleep(10)
```

### Explanation of why my code for ambulance.py was not working

- **Error 1 : ETA format wrong:** `"eta": 6` stores just a number. The hospital display expects `"eta": "6 minutes"` — a descriptive string with units. Without the units, the hospital screen shows just `6` with no context.
- **Error 2 : Missing ambulance ID field:** The system plan specifies that every message should include the ambulance identifier (e.g. `"ambulance": "A1"`). This field is absent, meaning the hospital cannot identify which ambulance is sending the data.
- **Error 3 (minor) : No client.loop_start():** Without `client.loop_start()`, the MQTT client's internal network thread is not running. This can cause messages to occasionally fail to send, especially on slower connections or when the broker is under load.

### Explanation of why my code for ambulance.py was not working

My code is now functionally close to correct. It connects to the broker, sends JSON-formatted data every 10 seconds, and prints confirmation. The remaining issues I am facing currently are about the data quality and completeness rather than fundamental logic errors.

---

### Team Message (Microsoft Teams — 18/03/2026)

> **Me:** Good Afternoon, My ambulance code is running now and I can see it printing "Data sent" every 10 seconds. But when I checked against the plan document, I noticed I'm missing the ambulance ID in the message and the ETA is just a number. Member B, does your hospital.py expect these fields in a specific format? I want to make sure my output matches what exacly the ambulance.py needs

---

### Member B Response

> **Kosi Ujam:** Yes, in my hospital.py I print `data['ambulance']` for the ambulance ID. If that field is missing in your message, it'll throw a KeyError when I try to display it. Please add `"ambulance": "A1"` to the dictionary. For ETA I display it as a string so `"6 minutes"` format would work better.

---

### Member A Response

> **Mohamad Radwan:** Also worth adding `client.loop_start()` after connect, I had issues with messages not sending reliably without it. It starts the background network thread, which then later on will allow the messages to be realiable to send.

---

### Member C Response

> **Mario Brunovsky:** For the database, I'm storing ETA as TEXT in SQLite so a string like "6 minutes" is fine. Just make sure you're consistent across what the assignment brief asks you.

---

## Iteration 4, Final Working Code ✅

### Date: Week 5 (approx. 24/03/2026)

### Code

```python
import paho.mqtt.client as mqtt
import json
import time
import random

# ── MQTT Configuration ──────────────────────────────────────
BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

# ── Ambulance Details ────────────────────────────────────────
AMBULANCE_ID = "A1"
PARAMEDIC = "Tobias Gonzalez"
TREATMENTS = [
    "Leg stabilised",
    "Oxygen administered",
    "Pain relief given",
    "Bandage applied",
    "Neck brace fitted"
]

# ── Patient Data Simulation ──────────────────────────────────
def get_patient_data():
    conditions = ["Broken Leg", "Chest Pain", "Broken Arm", "Head Injury"]
    return {
        "patient_id": 2,
        "condition": random.choice(conditions),
        "heart_rate": random.randint(70, 110),
        "oxygen": random.randint(90, 99),
        "status": random.choice(["Stable", "Critical"])
    }

# ── Build and Send Message ───────────────────────────────────
def send_data(client):
    patient = get_patient_data()
    eta = random.randint(3, 10)
    treatment = random.choice(TREATMENTS)

    message = {
        "ambulance":  AMBULANCE_ID,
        "patient_id": patient["patient_id"],
        "condition":  patient["condition"],
        "heart_rate": patient["heart_rate"],
        "oxygen":     patient["oxygen"],
        "status":     patient["status"],
        "eta":        f"{eta} minutes",
        "paramedic":  PARAMEDIC,
        "treatment":  treatment
    }

    payload = json.dumps(message)
    client.publish(TOPIC, payload)

    print(f"\n[Ambulance {AMBULANCE_ID}] Message sent at {time.strftime('%H:%M:%S')}")
    print(payload)

# ── MQTT Callbacks ───────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Connected to MQTT Broker successfully.")
    else:
        print(f"✗ Connection failed — return code {rc}")

# ── Main ─────────────────────────────────────────────────────
client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

print(f"Ambulance {AMBULANCE_ID} running. Sending data every 10 seconds...")
while True:
    send_data(client)
    time.sleep(10)
```

### All Errors I Resolved Thanks To The Feedbacks From My Peers

| Error | Status |
|-------|--------|
| Syntax errors (missing quotes, colons, commas) | ✅ Fixed in Iteration 2 |
| MQTT client not created or connected | ✅ Fixed in Iteration 2 |
| json.dump vs json.dumps | ✅ Fixed in Iteration 2 |
| Publishing dict instead of JSON string | ✅ Fixed in Iteration 2 |
| heart_rate stored as string | ✅ Fixed in Iteration 3 |
| No loop — only sent once | ✅ Fixed in Iteration 3 |
| ETA missing units | ✅ Fixed in Iteration 4 |
| Ambulance ID missing from message | ✅ Fixed in Iteration 4 |
| client.loop_start() missing | ✅ Fixed in Iteration 4 |

---

## My GitHub Commit History 

```
1. "Initial project structure and README"                     — Week 2
2. "Add first attempt at ambulance.py"                        — Week 2
3. "Fix syntax errors in ambulance.py after team feedback"    — Week 3
4. "Resolve MQTT connection and JSON formatting issues"        — Week 3
5. "Add continuous send loop and fix data types"               — Week 4
6. "Add ambulance ID, fix ETA format, add loop_start"         — Week 4
7. "Final working ambulance system"                           — Week 5
8. "Add MQTT test script and full debug log"                  — Week 6
```

---

## GitHub Issues Reference

| Issue | Resolution Commit |
|-------|-------------------|
| #1 — Fix syntax errors in ambulance.py | Commit: "Fix syntax errors after team feedback" |
| #2 — Ambulance not connecting to broker | Commit: "Resolve MQTT connection and JSON issues" |
| #3 — Hospital not receiving ambulance data | Commit: "Final working ambulance system" |
| #4 — Missing ambulance ID in message | Commit: "Add ambulance ID, fix ETA format" |

---

*Log maintained by Akujiezec (Chidera Akujieze) | Smart Ambulance System | Coventry University 2026*

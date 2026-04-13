# main.py Debug Log
**Developer:** Chidera Akujieze
**File:** main.py
**What it does:** runs the whole system from one place + fixes bugs I found in other files
**Period:** Week 4 to Week 6

---

## Summary of bugs I found and fixed

| Bug | Where | What happened | Fixed? |
|-----|-------|---------------|--------|
| FIX-01 | hospital.py | called wrong function name | yes |
| FIX-02 | ambulance.py vs hospital.py | different brokers | yes |
| FIX-03 | ambulance.py → database.py | key names didnt match | yes |
| FIX-04 | hospital_login.py | code was duplicated and broken | yes |

---

## FIX-01 — hospital.py was calling a function that doesnt exist

**File:** hospital.py
**When I found it:** Week 4 when I tried to run hospital.py and ambulance.py together

So basically when I was putting everything together I noticed hospital.py had this line:

```python
database.save_record(data)
```

However, when I went to look at database.py there is no function called save_record anywhere. The actual function is called save_data. So every single time the hospital received a message it would just crash immediately with this error:

```
AttributeError: module 'database' has no attribute 'save_record'
```

It basically meant no patient data was ever being saved at all which is a pretty big problem. I fixed it in main.py by using the correct function name:

```python
database.save_data(data)   # this is the right one
```

---

## FIX-02 — ambulance and hospital were connecting to completely different brokers

**Files:** ambulance.py and hospital.py
**When I found it:** Week 4, I noticed no messages were showing up on the hospital side

This one took me a while to figure out. The ambulance was running, the hospital was running, no errors anywhere, but the hospital wasnt showing any updates. Then I looked more carefully at both files and saw this:

ambulance.py had:
```python
BROKER = "test.mosquitto.org"
```

hospital.py had:
```python
BROKER = "localhost"
```

They were literally connecting to two completely different brokers. The ambulance was sending messages to a public broker on the internet and the hospital was listening on my own laptop. Obviously nothing was ever going to arrive. I fixed it in main.py by making both use the same broker:

```python
BROKER = "test.mosquitto.org"   # same for both now
```

---

## FIX-03 — the key names from ambulance.py didnt match what database.py was expecting

**Files:** ambulance.py → database.py
**When I found it:** Week 5, I noticed the database had loads of N/A and 0 values

So the ambulance sends data with key names like this (all lowercase):
```python
{ "patient_id": 2, "heart_rate": 92, "oxygen": 95 }
```

But database.py was trying to read the data with these key names (capital letters with spaces):
```python
data.get("Patient ID")
data.get("Heart Rate")
data.get("Oxygen Level")
```

Python is case sensitive so "heart_rate" is completely different from "Heart Rate". The database was getting None for every single field and using the default values instead (N/A and 0). The system looked like it was working but was actually just saving empty rows.

I fixed this by writing a small function in main.py that converts the keys before saving:

```python
def _map_keys_for_db(data):
    return {
        "Patient ID":   str(data.get("patient_id", "N/A")),
        "Heart Rate":   data.get("heart_rate", 0),
        "Oxygen Level": data.get("oxygen", 0),
        # etc
    }
```

Then calling database.save_data(_map_keys_for_db(data)) instead of passing the raw data.

---

## FIX-04 — hospital_login.py was completely broken / duplicated

**File:** hospital_login.py
**When I found it:** Week 5 when i tried to import it

This was the worst one to look at. The file had the same code copy-pasted in it like 3 or 4 times. The imports (import sqlite3, import hashlib) were not at the top of the file, they were randomly in the middle. And the menu() function was calling login_user() before login_user() was even defined which in some cases causes a NameError.

I didnt try to fix hospital_login.py itself because it was too messy. Instead I just rewrote the login logic cleanly inside main.py. I put all the helper functions (hash_password, create_database, register_user, login_user) at the top before anything calls them. The pre-seeded accounts mean it works straight away without having to register first.

---

## Other changes in main.py

- Used threading.Event() for shutdown instead of while True so Ctrl+C works properly
- Added try/except around both thread functions so errors print to screen instead of disappearing
- Added a 2 second wait before starting the hospital so the ambulance has time to connect first
- Pre-seeded 3 default accounts on first run (admin/hospital123, Tobias/123456, doctor/pass2026)

---

## Commit history

```
1. "add initial main.py launcher"                                — Week 4
2. "fix hospital calling wrong database function (FIX-01)"       — Week 4
3. "fix broker mismatch between ambulance and hospital (FIX-02)" — Week 5
4. "add key mapping function to fix database saving (FIX-03)"    — Week 5
5. "rewrite login system cleanly in main.py (FIX-04)"            — Week 5
6. "add threading event and clean shutdown"                       — Week 6
7. "final working main.py all fixes confirmed"                   — Week 6
```

---

*Chidera Akujieze | smart-ambulance- | Coventry University 2026*

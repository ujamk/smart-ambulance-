# 🚑 Smart Ambulance System – Simple Team Guide

## 📌 Purpose of This Guide

This guide explains **how our system works**, **what each file does**, and **what each person needs to build**.

If you are unsure what to do, follow this guide.

---

# 🧠 1. How the System Works (Simple Explanation)

Our system simulates an ambulance taking a patient to the hospital.

While the ambulance is travelling:

* The patient’s health is monitored
* The ambulance sends this data to the hospital
* The hospital receives the data and saves it

---

## 🔄 System Flow

Patient Monitor → Ambulance → MQTT → Hospital → Database

---

## 🪜 Step-by-step

1. Patient Monitor creates patient data
2. Ambulance collects the data
3. Ambulance sends it using MQTT
4. Hospital receives the data
5. Hospital shows it on screen
6. Hospital saves it in the database
7. This repeats every 10 seconds

---

# 📁 2. Project Structure (What each folder is for)

## 📂 src/ (MAIN CODE)

This is where all the system code goes.

Each person will work on ONE file here.

---

## 📂 docs/ (DOCUMENTATION)

This is where we write:

* weekly logs
* meeting notes

---

## 📂 tests/ (OPTIONAL)

This is for testing code (not very important for now, simple test file is enough).

---

## 📄 README.md

Explains the project to the lecturer.

---

## 📄 requirements.txt

Lists libraries needed for the system (like MQTT).

---

## 📄 system_guide.md

Guides the team on what each person should do and gives them an overall overview of how the system, repository structure and files works.

---

# 🧩 3. What Each File Must Do

---

## 🟢 patient_monitor.py (Mohamad Radwan)

This file creates fake patient data.

It should generate:

* heart rate
* oxygen level
* condition (broken leg, etc.)
* status (Stable / Critical)

### MUST HAVE:

```
def get_patient_data():
```

This function should RETURN data like this:

```
{
  "condition": "Broken Leg",
  "heart_rate": 90,
  "oxygen": 95,
  "status": "Stable"
}
```

---

## 🟢 ambulance.py (Chidera Akujieze)

This file represents the ambulance.

It should:

* get data from patient_monitor
* add extra info:

  * ETA
  * paramedic name
  * treatment
* send data using MQTT

### MUST HAVE:

```
def start_ambulance():
```

---

## 🟢 hospital.py (Kosi Ujam)

This file represents the hospital.

It should:

* receive data from MQTT
* display it on screen
* send it to the database

### MUST HAVE:

```
def start_hospital():
```

---

## 🟢 database.py (Mario Brunovsky)

This file stores patient data.

It should:

* save data into a database (or simple file)

### MUST HAVE:

```
def save_data(data):
```

---

## 🟢 hospital_login.py (Kosi Ujam)

This file handles login.

It should:

* ask for username/password
* allow access if correct

### MUST HAVE:

```
def login():
```

---

# 🚀 4. IMPORTANT: main.py (Runs Everything)

We will create:

```
src/main.py
```

This file will run the whole system. Every file must have at least ONE main function so that the main.py can run it

---

## 🧠 What it does

* starts hospital system
* starts ambulance system
* runs both at the same time

---

## ⚠️ IMPORTANT RULE

👉 DO NOT copy your code into main.py

👉 main.py will just CALL your functions

---

# ⚠️ 5. VERY IMPORTANT RULES (READ THIS)

---

## ❌ DO NOT DO THIS

```
print("Starting ambulance")
```

at the top level

👉 This will break the system

---

## ✅ DO THIS INSTEAD

Put your code inside a function:

```
def start_ambulance():
    print("Starting ambulance")
```

---

## ✅ ADD THIS AT THE BOTTOM

```
if __name__ == "__main__":
    start_ambulance()
```

---

## 🧠 WHY?

So:

* file runs normally when tested
* but does NOT run automatically when main.py imports it

---

# ▶️ 6. How to Run the System

When everything is ready:

```
python src/main.py
```

---

# 📌 7. What To Do Now (Team Tasks)

Each member should:

1. Open their file in `src/`
2. Create the required function
3. Make it work 
4. Test it
5. Commit changes to GitHub

---

# 🎯 FINAL GOAL

We want a system where:

✔ patient data is created
✔ ambulance sends data
✔ hospital receives it
✔ database stores it

---

# 💬 Final Note

Keep everything simple first.
If something does not work, ask in the group chat.
We will fix problems together.

---

✔ This guide should help everyone understand what to do.

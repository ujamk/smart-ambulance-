# 🚑 Smart Ambulance System

## 📌 Project Overview
This project is a Smart Ambulance System developed as part of a group assignment.  
The system simulates an ambulance transporting a patient to a hospital while sending real-time patient data using MQTT.

The goal is to help the hospital prepare for the patient before arrival by monitoring their condition during transportation.

---

## ⚙️ What the System Does

The system allows the hospital to:

- Receive real-time patient updates from the ambulance
- Display patient information on screen
- Store patient data in a database
- Track ambulance Estimated Time of Arrival (ETA)
- Identify the paramedic attending the patient
- Record treatment or first aid given
- Show the patient’s overall condition (e.g., broken leg, chest pain)
- Display a simple terminal dashboard (UI)

---

## 🧠 System Explanation (Step-by-Step)

1. The patient is monitored using a Patient Monitor system.
2. The system generates data such as:
   - Condition (e.g., Broken Leg)
   - Heart Rate
   - Oxygen Level
   - Status (Stable/Critical)

3. The ambulance collects this data and adds:
   - ETA (Estimated Time of Arrival)
   - Paramedic name
   - Treatment performed

4. The ambulance sends the data using MQTT.

5. The hospital receives the data.

6. The hospital:
   - Displays the data on screen
   - Stores it in the database

7. The system repeats every 10 seconds to simulate real-time monitoring.

---

## 🔄 System Flow

Patient Monitor → Ambulance → MQTT Broker → Hospital → Database

---

## 🖥️ Example Output

### Patient Monitor (UI)
SMART AMBULANCE MONITOR

Condition: Broken Leg
Heart Rate: 92 bpm
Oxygen Level: 95 %
Status: Stable
Next update in 10 seconds


---

### Ambulance System (Message Sent)

AMBULANCE A1 SENDING DATA...

Patient ID: 2
Condition: Broken Leg
Heart Rate: 92
Oxygen Level: 95
Status: Stable
ETA: 6 minutes
Paramedic: John Smith
Treatment: Leg stabilised


---

### Hospital System (Receiving Data)

PATIENT UPDATE RECEIVED

Patient ID: 2
Ambulance: A1
Condition: Broken Leg
Heart Rate: 92
Oxygen Level: 95
Status: Stable
ETA: 6 minutes
Paramedic: John Smith
Treatment: Leg stabilised


---

### Database Storage (Example Record)
Patient_data Table

patient_id: 2
condition: Broken Leg
heart_rate: 92
oxygen: 95
status: Stable
eta: 6
paramedic: John Smith
treatment: Leg stabilised
time: 10:00:10


---

### Continuous Updates Over Time

10:00:00 → Heart Rate: 90
10:00:10 → Heart Rate: 94
10:00:20 → Heart Rate: 88
10:00:30 → Heart Rate: 96


---

## 📁 Project Structure


src/
patient_monitor.py
ambulance.py
hospital.py
hospital_login.py
database.py

docs/
week1_log.md
ambulance_debug_log.md

tests/
test_mqtt.py


---

## ⚙️ Technologies Used

- Python
- MQTT (Paho MQTT)
- SQLite
- GitHub

---

## ▶️ How to Run the System

1. Install dependencies:

pip install paho-mqtt


2. Run the hospital system:

python src/hospital.py


3. Run the ambulance system:

python src/ambulance.py


---

## 👥 Team Members and Roles

- Mohamad Radwan → Patient Monitor (patient_monitor.py)
- Chidera Akujieze → Ambulance System (ambulance.py)
- Kosi Ujam → Hospital System + Login (hospital.py)
- Mario Brunovsky → Database System (database.py)

---

## 📊 Features Implemented

- Real-time data simulation
- MQTT communication
- Terminal-based UI
- Database storage
- Patient condition tracking
- ETA calculation
- Login system for hospital staff

---

## 🚀 Future Improvements

- Graphical User Interface (GUI)
- GPS tracking
- Real sensor integration
- Enhanced security system

---

## 📌 Notes

This project was developed following an agile approach, including task allocation, weekly progress tracking, and version control using GitHub.

### Patient Monitor (UI)

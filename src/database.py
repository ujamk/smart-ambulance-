import sqlite3
from datetime import datetime

DB_NAME = "hospital.db"

def init_db():
    """Create the patient_data table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_data (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  TEXT,
            condition   TEXT,
            heart_rate  INTEGER,
            oxygen      INTEGER,
            status      TEXT,
            eta         TEXT,
            paramedic   TEXT,
            treatment   TEXT,
            time        TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("[Database] Table ready.")

def save_data(data: dict):
    """
    Save a patient record to the database.
    Called by hospital.py each time a new MQTT message is received.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patient_data
            (patient_id, condition, heart_rate, oxygen, status, eta, paramedic, treatment, time)
        VALUES
            (:patient_id, :condition, :heart_rate, :oxygen, :status, :eta, :paramedic, :treatment, :time)
    ''', {
        "patient_id": data.get("Patient ID", "N/A"),
        "condition":  data.get("Condition", "N/A"),
        "heart_rate": data.get("Heart Rate", 0),
        "oxygen":     data.get("Oxygen Level", 0),
        "status":     data.get("Status", "N/A"),
        "eta":        data.get("ETA", "N/A"),
        "paramedic":  data.get("Paramedic", "N/A"),
        "treatment":  data.get("Treatment", "N/A"),
        "time":       datetime.now().strftime("%H:%M:%S")
    })
    conn.commit()
    conn.close()
    print(f"[Database] Record saved for Patient ID: {data.get('Patient ID', 'N/A')}")

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

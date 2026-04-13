import threading
import time
import json
import random
import sqlite3
import hashlib
import os
import sys
from datetime import datetime
from getpass import getpass

import paho.mqtt.client as mqtt

# ── Import project modules ──────────────────────────────────────────────────
import database        # database.py  – init_db / save_data / get_all_records
import patient_monitor # patient_monitor.py – generate_patient_data

# ── Shared MQTT Configuration (FIX-02: unified broker) ─────────────────────
BROKER = "test.mosquitto.org"   # was "localhost" in hospital.py  ← FIX-02
PORT   = 1883
TOPIC  = "ambulance/patient"

# ── Ambulance details (mirrors ambulance.py) ────────────────────────────────
AMBULANCE_ID = "A1"
PARAMEDIC    = "Tobias Gonzalez"
TREATMENTS   = [
    "Leg stabilised",
    "Oxygen administered",
    "Pain relief given",
    "Bandage applied",
    "Neck brace fitted",
]

# ── Login database (hospital_login.py – cleaned) ────────────────────────────
LOGIN_DB = "smart_ambulance_users.db"

def _hash_password(password: str) -> str:
    """SHA-256 hash for storing / comparing passwords."""
    return hashlib.sha256(password.encode()).hexdigest()

def _create_login_db() -> None:
    """Create the users table if it does not already exist."""
    conn = sqlite3.connect(LOGIN_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def _register_user(username: str, password: str, role: str = "staff") -> None:
    """Insert a new user; prints a message if the username already exists."""
    conn = sqlite3.connect(LOGIN_DB)
    try:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, _hash_password(password), role)
        )
        conn.commit()
        print(f"  ✓ User '{username}' registered as '{role}'.")
    except sqlite3.IntegrityError:
        print(f"  ✗ Username '{username}' already exists.")
    finally:
        conn.close()

def _login_user(username: str, password: str) -> bool:
    """Return True and print welcome if credentials are valid, else False."""
    conn = sqlite3.connect(LOGIN_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, _hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        print(f"\n  ✓ Login successful. Welcome, {user[0]} ({user[1]})!\n")
        return True
    print("  ✗ Invalid username or password.")
    return False

def run_login_menu() -> bool:
    """
    Interactive menu: register, login or exit.
    Returns True when a successful login occurs; False if the user exits.
    (FIX-04: functions were defined after the code that called them in
     hospital_login.py; this version defines helpers first.)
    """
    _create_login_db()

    # Pre-seed a default admin so the system works out of the box
    _register_user("admin",  "hospital123", "admin")
    _register_user("Tobias", "123456",      "paramedic")
    _register_user("doctor", "pass2026",    "doctor")

    while True:
        print("\n" + "=" * 40)
        print("   SMART AMBULANCE LOGIN SYSTEM")
        print("=" * 40)
        print("  1. Register new user")
        print("  2. Login")
        print("  3. Exit")
        choice = input("\n  Choose an option: ").strip()

        if choice == "1":
            username = input("  New username : ").strip()
            password = getpass("  New password : ").strip()
            role     = input("  Role (admin/staff/doctor/paramedic): ").strip() or "staff"
            if username and password:
                _register_user(username, password, role)
            else:
                print("  All fields are required.")

        elif choice == "2":
            username = input("  Username : ").strip()
            password = getpass("  Password : ").strip()
            if username and password:
                if _login_user(username, password):
                    return True
            else:
                print("  Username and password cannot be empty.")

        elif choice == "3":
            print("  Exiting system.")
            return False
        else:
            print("  Invalid option. Please try again.")


# ── Patient Monitor thread ──────────────────────────────────────────────────
def run_patient_monitor(stop_event: threading.Event) -> None:
    """
    Runs generate_patient_data() every 10 seconds and prints a dashboard.
    Uses the stop_event instead of an infinite loop so main() can shut it
    down cleanly.  Screen-clear is skipped in threaded mode to avoid
    overwriting other threads' output.
    """
    while not stop_event.is_set():
        condition, heart_rate, oxygen_level, status = patient_monitor.generate_patient_data()
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'─'*40}")
        print(f"  PATIENT MONITOR  [{timestamp}]")
        print(f"{'─'*40}")
        print(f"  Condition    : {condition}")
        print(f"  Heart Rate   : {heart_rate} bpm")
        print(f"  Oxygen Level : {oxygen_level} %")
        print(f"  Status       : {status}")
        print(f"{'─'*40}")
        stop_event.wait(timeout=10)  # sleep 10 s or until stop is signalled


# ── Ambulance MQTT publisher thread ────────────────────────────────────────
def _build_ambulance_message() -> dict:
    """Build one ambulance telemetry message (mirrors ambulance.py logic)."""
    condition, heart_rate, oxygen_level, status = patient_monitor.generate_patient_data()
    return {
        "ambulance":  AMBULANCE_ID,
        "patient_id": 2,
        "condition":  condition,
        "heart_rate": heart_rate,
        "oxygen":     oxygen_level,
        "status":     status,
        "eta":        f"{random.randint(3, 10)} minutes",
        "paramedic":  PARAMEDIC,
        "treatment":  random.choice(TREATMENTS),
    }

def run_ambulance(stop_event: threading.Event) -> None:
    """Connect to MQTT broker and publish a patient update every 10 seconds."""
    client = mqtt.Client()

    def on_connect(c, userdata, flags, rc):
        if rc == 0:
            print(f"\n  [Ambulance] ✓ Connected to broker [{BROKER}:{PORT}]")
        else:
            print(f"\n  [Ambulance] ✗ Connection failed (rc={rc})")

    client.on_connect = on_connect
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as exc:
        print(f"\n  [Ambulance] ✗ Could not reach broker: {exc}")
        return

    client.loop_start()

    while not stop_event.is_set():
        msg = _build_ambulance_message()
        client.publish(TOPIC, json.dumps(msg))
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"\n  [Ambulance {AMBULANCE_ID}] Sent at {ts}")
        for k, v in msg.items():
            print(f"    {k:<12}: {v}")
        stop_event.wait(timeout=10)

    client.loop_stop()
    client.disconnect()


# ── Key-mapping helper (FIX-03) ─────────────────────────────────────────────
def _map_keys_for_db(data: dict) -> dict:
    """
    ambulance.py publishes lowercase keys  ("patient_id", "heart_rate", …)
    but database.save_data() expected Title-Case keys ("Patient ID", …).
    This adapter normalises the payload so both sides agree.   ← FIX-03
    """
    return {
        "Patient ID":    str(data.get("patient_id", "N/A")),
        "Condition":     data.get("condition",  "N/A"),
        "Heart Rate":    data.get("heart_rate", 0),
        "Oxygen Level":  data.get("oxygen",     0),
        "Status":        data.get("status",     "N/A"),
        "ETA":           data.get("eta",        "N/A"),
        "Paramedic":     data.get("paramedic",  "N/A"),
        "Treatment":     data.get("treatment",  "N/A"),
    }


# ── Hospital MQTT subscriber (main thread after login) ──────────────────────
def run_hospital() -> None:
    """
    Subscribe to the ambulance topic, display each update and persist it.
    FIX-01: was calling database.save_record() which does not exist;
            corrected to database.save_data() with key mapping.
    FIX-02: broker changed from "localhost" to BROKER constant.
    """
    client = mqtt.Client()

    def on_connect(c, userdata, flags, rc):
        if rc == 0:
            print(f"  [Hospital] ✓ Connected to broker. Listening on '{TOPIC}' …\n")
            c.subscribe(TOPIC)
        else:
            print(f"  [Hospital] ✗ Broker connection failed (rc={rc})")

    def on_message(c, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            print("  [Hospital] ✗ Malformed JSON received – ignored.")
            return

        # ── Display update ──────────────────────────────────────────────
        status_col = "\033[91m" if data.get("status") == "Critical" else "\033[92m"
        rst        = "\033[0m"
        ts         = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*50}")
        print(f"  PATIENT UPDATE RECEIVED  [{ts}]")
        print(f"{'='*50}")
        print(f"  Ambulance    : {data.get('ambulance',  'N/A')}")
        print(f"  Patient ID   : {data.get('patient_id', 'N/A')}")
        print(f"  Condition    : {data.get('condition',  'N/A')}")
        print(f"  Heart Rate   : {data.get('heart_rate', 'N/A')} bpm")
        print(f"  Oxygen Level : {data.get('oxygen',     'N/A')} %")
        print(f"  Status       : {status_col}{data.get('status', 'N/A')}{rst}")
        print(f"  ETA          : {data.get('eta',        'N/A')}")
        print(f"  Paramedic    : {data.get('paramedic',  'N/A')}")
        print(f"  Treatment    : {data.get('treatment',  'N/A')}")
        print(f"{'='*50}")

        # ── Save to database (FIX-01 + FIX-03) ─────────────────────────
        database.save_data(_map_keys_for_db(data))  # FIX-01: was save_record()

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)   # FIX-02: was "localhost"
    except Exception as exc:
        print(f"  [Hospital] ✗ Could not reach broker: {exc}")
        return

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    print("\n" + "█" * 50)
    print("         SMART AMBULANCE SYSTEM  v1.0")
    print("█" * 50)

    # Step 1 – login
    if not run_login_menu():
        sys.exit(0)

    # Step 2 – initialise database
    database.init_db()

    stop_event = threading.Event()

    # Step 3 – start patient monitor in background thread
    monitor_thread = threading.Thread(
        target=run_patient_monitor,
        args=(stop_event,),
        daemon=True,
        name="PatientMonitor",
    )
    monitor_thread.start()

    # Step 4 – start ambulance publisher in background thread
    ambulance_thread = threading.Thread(
        target=run_ambulance,
        args=(stop_event,),
        daemon=True,
        name="Ambulance",
    )
    ambulance_thread.start()

    # Brief pause so the ambulance connects before the hospital subscribes
    time.sleep(2)

    # Step 5 – run hospital receiver on main thread (blocking)
    print("\n  Starting hospital monitoring system …")
    print("  Press Ctrl+C to stop.\n")
    try:
        run_hospital()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\n  Shutting down Smart Ambulance System …")
        stop_event.set()
        monitor_thread.join(timeout=5)
        ambulance_thread.join(timeout=5)
        print("  All systems stopped. Goodbye.\n")


if __name__ == "__main__":
    main()


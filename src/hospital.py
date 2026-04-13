import paho.mqtt.client as mqtt
import json
import time
import database

BROKER = "localhost"
PORT = 1883
TOPIC = "ambulance/patient"

VALID_USERS = {
    "admin": "hospital123",
    "Tobias": "123456",
    "doctor": "pass2026",
}


def login():
    print("=" * 40)
    print("       HOSPITAL SYSTEM LOGIN")
    print("=" * 40)

    attempts = 3

    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if VALID_USERS.get(username) == password:
            print(f"\nLogin successful. Welcome, {username}!\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect credentials. {attempts} attempt(s) remaining.\n")

    print("Access denied. Exiting.")
    return False


def display_patient_update(data):
    print("\n" + "=" * 50)
    print("PATIENT UPDATE RECEIVED")
    print("=" * 50)
    print(f"Ambulance: {data.get('ambulance', 'N/A')}")
    print(f"Patient ID: {data.get('patient_id', 'N/A')}")
    print(f"Condition: {data.get('condition', 'N/A')}")
    print(f"Heart Rate: {data.get('heart_rate', 'N/A')} bpm")
    print(f"Oxygen Level: {data.get('oxygen', 'N/A')} %")
    print(f"Status: {data.get('status', 'N/A')}")
    print(f"ETA: {data.get('eta', 'N/A')}")
    print(f"Paramedic: {data.get('paramedic', 'N/A')}")
    print(f"Treatment: {data.get('treatment', 'N/A')}")
    print("=" * 50)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker [{BROKER}:{PORT}]")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed — return code {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        display_patient_update(data)
        database.save_record(data)
    except json.JSONDecodeError:
        print("Received malformed message")


def main():
    if not login():
        return

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()from getpass import getpass


def menu():
    create_database()

    while True:
        print("\n--- Smart Ambulance Login System ---")
        print("1. Register user")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Enter new username: ").strip()
            password = getpass("Enter new password: ").strip()
            role = input("Enter role (e.g. admin/staff): ").strip()

            if username and password and role:
                register_user(username, password, role)
            else:
                print("All fields are required.")

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = getpass("Enter password: ").strip()

            if username and password:
                login_user(username, password)
            else:
                print("Username and password cannot be empty.")

        elif choice == "3":
            print("Exiting system.")
            break

        else:
            print("Invalid option. Please try again.")def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, hashed_pw)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Login successful. Welcome {user[0]} ({user[1]}).")
        return True
    else:
        print("Invalid username or password.")
        return False# Smart Ambulance Login System

import sqlite3
import hashlib

DB_NAME = "smart_ambulance_users.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password, role="staff"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
        print(f"User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()# Smart Ambulance Login System

import sqlite3
import hashlib

DB_NAME = "smart_ambulance_users.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password, role="staff"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
        print(f"User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()# Smart Ambulance Login System

import sqlite3
import hashlib

DB_NAME = "smart_ambulance_users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()# Smart Ambulance Login System

import sqlite3
import hashlib

DB_NAME = "smart_ambulance_users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Smart Ambulance Login System

import sqlite3
import hashlib
from getpass import getpass

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
        conn.close()


def login_user(username, password):
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
        return False


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
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()

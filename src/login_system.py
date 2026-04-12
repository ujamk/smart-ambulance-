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

# Smart Ambulance Login System

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

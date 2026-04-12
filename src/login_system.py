# Smart Ambulance Login System

import sqlite3
import hashlib

DB_NAME = "smart_ambulance_users.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

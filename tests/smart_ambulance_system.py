import unittest
import sqlite3
import os
import json
import hashlib
import sys
import time
from unittest.mock import patch, MagicMock

# ── Make sure the project root is on the path ───────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Import modules under test ────────────────────────────────────────────────
import database
import patient_monitor


# ═══════════════════════════════════════════════════════════════════════════════
#  1. DATABASE TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestDatabase(unittest.TestCase):
    """Tests for database.py – table creation, insert and retrieval."""

    TEST_DB = "test_hospital.db"

    def setUp(self):
        """Point the database module at a fresh test database before each test."""
        database.DB_NAME = self.TEST_DB
        database.init_db()

    def tearDown(self):
        """Remove the test database file after each test."""
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    # ── init_db ────────────────────────────────────────────────────────────
    def test_init_db_creates_table(self):
        """init_db() must create the patient_data table."""
        conn = sqlite3.connect(self.TEST_DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patient_data'"
        )
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result, "Table 'patient_data' was not created by init_db().")

    def test_init_db_is_idempotent(self):
        """Calling init_db() twice should not raise an error."""
        try:
            database.init_db()  # second call
        except Exception as exc:
            self.fail(f"init_db() raised on second call: {exc}")

    # ── save_data ──────────────────────────────────────────────────────────
    def _sample_record(self, patient_id="2"):
        return {
            "Patient ID":   patient_id,
            "Condition":    "Broken Leg",
            "Heart Rate":   92,
            "Oxygen Level": 95,
            "Status":       "Stable",
            "ETA":          "6 minutes",
            "Paramedic":    "Tobias Gonzalez",
            "Treatment":    "Leg stabilised",
        }

    def test_save_data_inserts_row(self):
        """save_data() should insert exactly one row."""
        database.save_data(self._sample_record())
        rows = database.get_all_records()
        self.assertEqual(len(rows), 1, "Expected 1 row after one save_data() call.")

    def test_save_data_stores_correct_values(self):
        """Saved values should match what was passed in."""
        database.save_data(self._sample_record())
        rows = database.get_all_records()
        row = rows[0]
        # Columns: id, patient_id, condition, heart_rate, oxygen, status, eta, paramedic, treatment, time
        self.assertEqual(row[1], "2",             "patient_id mismatch")
        self.assertEqual(row[2], "Broken Leg",    "condition mismatch")
        self.assertEqual(row[3], 92,              "heart_rate mismatch")
        self.assertEqual(row[4], 95,              "oxygen mismatch")
        self.assertEqual(row[5], "Stable",        "status mismatch")
        self.assertEqual(row[6], "6 minutes",     "eta mismatch")
        self.assertEqual(row[7], "Tobias Gonzalez","paramedic mismatch")
        self.assertEqual(row[8], "Leg stabilised","treatment mismatch")

    def test_save_data_multiple_records(self):
        """Multiple records should all be stored independently."""
        database.save_data(self._sample_record("1"))
        database.save_data(self._sample_record("2"))
        database.save_data(self._sample_record("3"))
        rows = database.get_all_records()
        self.assertEqual(len(rows), 3, "Expected 3 rows for 3 save_data() calls.")

    def test_save_data_missing_keys_use_defaults(self):
        """save_data() should not crash when optional keys are absent."""
        try:
            database.save_data({})   # empty dict – all fields will be default
        except Exception as exc:
            self.fail(f"save_data({{}}) raised unexpectedly: {exc}")
        rows = database.get_all_records()
        self.assertEqual(len(rows), 1)

    # ── get_all_records ────────────────────────────────────────────────────
    def test_get_all_records_empty(self):
        """Fresh database should return an empty list."""
        rows = database.get_all_records()
        self.assertEqual(rows, [], "Expected empty list for a fresh database.")

    def test_get_all_records_returns_list(self):
        """get_all_records() must always return a list (never None)."""
        result = database.get_all_records()
        self.assertIsInstance(result, list)


# ═══════════════════════════════════════════════════════════════════════════════
#  2. PATIENT MONITOR TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestPatientMonitor(unittest.TestCase):
    """Tests for patient_monitor.py – data generation and status logic."""

    VALID_CONDITIONS = {"Broken Leg", "Broken Arm", "Chest Pain", "Head Injury", "Severe Burn"}
    VALID_STATUSES   = {"Stable", "Critical"}

    def test_generate_patient_data_returns_four_values(self):
        """generate_patient_data() must return a 4-tuple."""
        result = patient_monitor.generate_patient_data()
        self.assertEqual(len(result), 4, "Expected tuple of 4 values.")

    def test_condition_is_valid(self):
        """Condition must be one of the defined conditions."""
        for _ in range(20):
            condition, _, _, _ = patient_monitor.generate_patient_data()
            self.assertIn(condition, self.VALID_CONDITIONS,
                          f"Unexpected condition: {condition}")

    def test_heart_rate_in_range(self):
        """Heart rate must be between 60 and 140 bpm."""
        for _ in range(50):
            _, heart_rate, _, _ = patient_monitor.generate_patient_data()
            self.assertGreaterEqual(heart_rate, 60,  f"Heart rate too low: {heart_rate}")
            self.assertLessEqual(heart_rate,   140,  f"Heart rate too high: {heart_rate}")

    def test_oxygen_level_in_range(self):
        """Oxygen level must be between 88 % and 100 %."""
        for _ in range(50):
            _, _, oxygen_level, _ = patient_monitor.generate_patient_data()
            self.assertGreaterEqual(oxygen_level, 88,  f"Oxygen too low: {oxygen_level}")
            self.assertLessEqual(oxygen_level,   100,  f"Oxygen too high: {oxygen_level}")

    def test_status_is_valid(self):
        """Status must be either 'Stable' or 'Critical'."""
        for _ in range(50):
            _, _, _, status = patient_monitor.generate_patient_data()
            self.assertIn(status, self.VALID_STATUSES,
                          f"Unexpected status: {status}")

    def test_status_critical_when_heart_rate_high(self):
        """Status must be 'Critical' when heart rate > 120."""
        with patch("random.randint") as mock_randint, \
             patch("random.choice", return_value="Chest Pain"):
            # heart_rate = 130, oxygen_level = 95
            mock_randint.side_effect = [130, 95]
            _, _, _, status = patient_monitor.generate_patient_data()
            self.assertEqual(status, "Critical",
                             "Expected Critical for heart_rate=130")

    def test_status_critical_when_oxygen_low(self):
        """Status must be 'Critical' when oxygen level < 92."""
        with patch("random.randint") as mock_randint, \
             patch("random.choice", return_value="Chest Pain"):
            # heart_rate = 80, oxygen_level = 89
            mock_randint.side_effect = [80, 89]
            _, _, _, status = patient_monitor.generate_patient_data()
            self.assertEqual(status, "Critical",
                             "Expected Critical for oxygen=89")

    def test_status_stable_when_vitals_normal(self):
        """Status must be 'Stable' when all vitals are within normal range."""
        with patch("random.randint") as mock_randint, \
             patch("random.choice", return_value="Broken Leg"):
            # heart_rate = 80, oxygen_level = 97
            mock_randint.side_effect = [80, 97]
            _, _, _, status = patient_monitor.generate_patient_data()
            self.assertEqual(status, "Stable",
                             "Expected Stable for heart_rate=80, oxygen=97")

    def test_generate_patient_data_is_random(self):
        """Repeated calls should not always return identical results (probabilistic)."""
        results = set()
        for _ in range(30):
            condition, hr, ox, _ = patient_monitor.generate_patient_data()
            results.add((condition, hr, ox))
        self.assertGreater(len(results), 1,
                           "generate_patient_data() appears to always return the same values.")


# ═══════════════════════════════════════════════════════════════════════════════
#  3. AMBULANCE MESSAGE TESTS  (logic only – no live MQTT)
# ═══════════════════════════════════════════════════════════════════════════════
class TestAmbulanceMessage(unittest.TestCase):
    """
    Tests the message structure ambulance.py would produce.
    We replicate the ambulance logic here so no MQTT connection is needed.
    """

    REQUIRED_KEYS = {
        "ambulance", "patient_id", "condition", "heart_rate",
        "oxygen", "status", "eta", "paramedic", "treatment",
    }

    def _build_message(self):
        """Mirror of ambulance.py's send_data logic."""
        condition, heart_rate, oxygen_level, status = patient_monitor.generate_patient_data()
        import random
        return {
            "ambulance":  "A1",
            "patient_id": 2,
            "condition":  condition,
            "heart_rate": heart_rate,
            "oxygen":     oxygen_level,
            "status":     status,
            "eta":        f"{random.randint(3, 10)} minutes",
            "paramedic":  "Tobias Gonzalez",
            "treatment":  "Leg stabilised",
        }

    def test_message_contains_all_required_keys(self):
        """Every ambulance message must contain all required fields."""
        msg = self._build_message()
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, msg, f"Missing required key: '{key}'")

    def test_message_serialises_to_json(self):
        """Message dict must be serialisable to JSON without errors."""
        msg = self._build_message()
        try:
            payload = json.dumps(msg)
        except (TypeError, ValueError) as exc:
            self.fail(f"json.dumps() failed: {exc}")
        self.assertIsInstance(payload, str)

    def test_message_deserialises_correctly(self):
        """A JSON round-trip must return an equal dictionary."""
        original = self._build_message()
        recovered = json.loads(json.dumps(original))
        self.assertEqual(original, recovered)

    def test_patient_id_is_integer(self):
        """patient_id must be an integer (not a string)."""
        msg = self._build_message()
        self.assertIsInstance(msg["patient_id"], int)

    def test_eta_contains_minutes(self):
        """ETA string must contain the word 'minutes'."""
        for _ in range(10):
            msg = self._build_message()
            self.assertIn("minutes", msg["eta"], f"ETA format wrong: {msg['eta']}")


# ═══════════════════════════════════════════════════════════════════════════════
#  4. KEY MAPPING TESTS  (FIX-03 adapter function)
# ═══════════════════════════════════════════════════════════════════════════════
class TestKeyMapping(unittest.TestCase):
    """
    Verifies the _map_keys_for_db() adapter introduced in main.py (FIX-03).
    We inline the function here so this test file is self-contained.
    """

    @staticmethod
    def _map_keys_for_db(data: dict) -> dict:
        """Exact copy of the function from main.py."""
        return {
            "Patient ID":   str(data.get("patient_id", "N/A")),
            "Condition":    data.get("condition",  "N/A"),
            "Heart Rate":   data.get("heart_rate", 0),
            "Oxygen Level": data.get("oxygen",     0),
            "Status":       data.get("status",     "N/A"),
            "ETA":          data.get("eta",        "N/A"),
            "Paramedic":    data.get("paramedic",  "N/A"),
            "Treatment":    data.get("treatment",  "N/A"),
        }

    SAMPLE_AMBULANCE_PAYLOAD = {
        "ambulance":  "A1",
        "patient_id": 2,
        "condition":  "Broken Leg",
        "heart_rate": 92,
        "oxygen":     95,
        "status":     "Stable",
        "eta":        "6 minutes",
        "paramedic":  "Tobias Gonzalez",
        "treatment":  "Leg stabilised",
    }

    def test_patient_id_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["Patient ID"], "2")

    def test_condition_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["Condition"], "Broken Leg")

    def test_heart_rate_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["Heart Rate"], 92)

    def test_oxygen_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["Oxygen Level"], 95)

    def test_status_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["Status"], "Stable")

    def test_eta_mapped(self):
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertEqual(mapped["ETA"], "6 minutes")

    def test_defaults_on_empty_payload(self):
        """Empty payload should give safe defaults, not KeyError."""
        mapped = self._map_keys_for_db({})
        self.assertEqual(mapped["Patient ID"],   "N/A")
        self.assertEqual(mapped["Heart Rate"],    0)
        self.assertEqual(mapped["Oxygen Level"],  0)

    def test_patient_id_is_string_after_mapping(self):
        """Patient ID should always be a string after mapping."""
        mapped = self._map_keys_for_db(self.SAMPLE_AMBULANCE_PAYLOAD)
        self.assertIsInstance(mapped["Patient ID"], str)


# ═══════════════════════════════════════════════════════════════════════════════
#  5. LOGIN SYSTEM TESTS
# ═══════════════════════════════════════════════════════════════════════════════
class TestLoginSystem(unittest.TestCase):
    """
    Tests the hashed-password login logic from hospital_login.py / main.py.
    Uses a separate temporary database to avoid touching production data.
    """

    TEST_DB = "test_users.db"

    # ── inline minimal login functions (same logic as main.py) ──────────────
    def _hash(self, pw: str) -> str:
        return hashlib.sha256(pw.encode()).hexdigest()

    def _create_db(self):
        conn = sqlite3.connect(self.TEST_DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _register(self, username, password, role="staff"):
        conn = sqlite3.connect(self.TEST_DB)
        try:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, self._hash(password), role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def _login(self, username, password):
        conn = sqlite3.connect(self.TEST_DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, role FROM users WHERE username = ? AND password = ?",
            (username, self._hash(password))
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None

    # ── setUp / tearDown ────────────────────────────────────────────────────
    def setUp(self):
        self._create_db()

    def tearDown(self):
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    # ── tests ───────────────────────────────────────────────────────────────
    def test_register_new_user(self):
        """Registering a new user should succeed."""
        result = self._register("alice", "secret", "doctor")
        self.assertTrue(result, "register() returned False for a new user.")

    def test_register_duplicate_username(self):
        """Registering the same username twice should fail gracefully."""
        self._register("bob", "pass1", "staff")
        result = self._register("bob", "pass2", "staff")
        self.assertFalse(result, "Duplicate username should return False.")

    def test_login_correct_credentials(self):
        """Login with correct username and password should succeed."""
        self._register("carol", "mypassword", "admin")
        result = self._login("carol", "mypassword")
        self.assertTrue(result, "Login failed with correct credentials.")

    def test_login_wrong_password(self):
        """Login with wrong password must fail."""
        self._register("dave", "correcthorse", "staff")
        result = self._login("dave", "wrongpassword")
        self.assertFalse(result, "Login should fail with an incorrect password.")

    def test_login_nonexistent_user(self):
        """Login for a user that was never registered must fail."""
        result = self._login("ghost", "anything")
        self.assertFalse(result)

    def test_password_is_hashed_in_db(self):
        """Plaintext password must NOT appear in the database."""
        self._register("eve", "plaintextpassword", "staff")
        conn = sqlite3.connect(self.TEST_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = 'eve'")
        stored = cursor.fetchone()[0]
        conn.close()
        self.assertNotEqual(stored, "plaintextpassword",
                            "Password stored as plaintext – must be hashed!")
        self.assertEqual(len(stored), 64,
                         "Expected a 64-character SHA-256 hex digest.")

    def test_login_is_case_sensitive(self):
        """Username and password comparisons must be case-sensitive."""
        self._register("Frank", "Password1", "staff")
        self.assertFalse(self._login("frank", "Password1"), "Username should be case-sensitive.")
        self.assertFalse(self._login("Frank", "password1"), "Password should be case-sensitive.")
        self.assertTrue(self._login("Frank", "Password1"),  "Exact credentials should work.")


# ═══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)

